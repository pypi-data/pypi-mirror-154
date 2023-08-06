import setuptools

from wynncraft import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wynncraft",
    version=__version__,
    author="Martin Kovács",
    author_email="martin.k.kovacs@gmail.com",
    description="A wrapper for the Wynncraft API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martinkovacs/wynncraft-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
