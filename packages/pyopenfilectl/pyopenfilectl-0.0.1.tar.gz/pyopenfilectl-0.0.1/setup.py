from setuptools import setup, find_packages

from openfilectl import __version__

setup(
    name="pyopenfilectl",
    version=__version__,
    author="greene",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "httpx",
        "aiofiles",
        "click",
        "tqdm",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "pip-tools",
        ],
    },
    entry_points={"console_scripts": ["openfilectl=openfilectl.__main__:main"]},
)
