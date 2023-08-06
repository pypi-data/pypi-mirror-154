import os
import logging
import hashlib
import asyncio
import concurrent.futures
from datetime import datetime

import click
import httpx
import aiofiles
from aiofiles import os as aios
from tqdm import tqdm

from openfilectl import __version__

logger = logging.getLogger(__name__)
openfile_server = os.environ.get("openfile_server", "http://localhost:8000")
max_concurrent_upload_num = os.environ.get("max_concurrent_upload_num", 256)


@click.group()
def cli():
    pass


@cli.command()
def version():
    print(__version__)


@cli.command()
@click.option("--file", "-f", required=True, help="upload file name or dir name")
def upload(file):
    filepath = os.path.abspath(file)

    start_time = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        if os.path.isfile(filepath):
            asyncio.run(async_upload_file(filepath, pool))
        else:
            asyncio.run(async_upload_files(filepath, pool))

    end_time = datetime.now()
    t = end_time - start_time
    print(f"time: {t}")


@cli.command()
@click.option("--file", "-f", required=True, help="download file name")
@click.option("--download-dir", help="download root dir")
def download(file, download_dir):
    asyncio.run(async_download_file(file, download_dir))
    print("download completed.")


async def async_upload_files(root, threadpool):
    loop = asyncio.get_running_loop()

    fs = await loop.run_in_executor(None, list_all_files, root)

    tasks = []
    sem = asyncio.Semaphore(max_concurrent_upload_num, loop=loop)

    for f in fs:
        task = asyncio.create_task(async_upload_file(f, threadpool, semaphore=sem))
        tasks.append(task)

    await asyncio.gather(*tasks)


def list_all_files(root):
    fs = []

    def list_files(dir):
        for root, dirs, files in os.walk(dir):
            for f in files:
                fs.append(os.path.join(root, f))

            for d in dirs:
                list_files(d)

    list_files(root)

    return fs


def semaphore(func):
    async def inner(*args, **kwargs):
        sem = kwargs.get("semaphore", None)

        if sem is None:
            return await func(*args, **kwargs)
        else:
            async with sem:
                return await func(*args, **kwargs)

    return inner


@semaphore
async def async_upload_file(filepath, threadpool, **kwargs):
    loop = asyncio.get_running_loop()

    filename = os.path.basename(filepath)
    if not await aios.path.exists(filepath):
        raise Exception("the file is not exists, path: {filepath}")

    hash = await loop.run_in_executor(
        threadpool,
        sum_file_hash,
        filepath,
    )

    async with aiofiles.open(filepath, "rb") as f:
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{openfile_server}/objects/{filename}",
                data=f,
                headers={"digest": f"sha256={hash}"},
            )

            if resp.status_code != 200:
                raise Exception(
                    f"upload failed, code: {resp.status_code}, content: {resp.content}, filename: {filename}, hash: {hash}"
                )


async def async_download_file(filename, download_dir=None):
    if download_dir is not None:
        download_dir = os.path.abspath(download_dir)
        if not await aios.path.exists(download_dir):
            await aios.mkdir(download_dir)

        filepath = os.path.join(download_dir, filename)
    else:
        filepath = os.path.join(os.getcwd(), filename)

    async with aiofiles.open(filepath, "wb") as f:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "GET", f"{openfile_server}/objects/{filename}"
            ) as resp:
                total = int(resp.headers["Content-Length"])
                with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                    num_bytes_downloaded = resp.num_bytes_downloaded
                    async for chunk in resp.aiter_bytes():
                        await f.write(chunk)
                        progress.update(resp.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = resp.num_bytes_downloaded


def sum_file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
        return h.hexdigest()
