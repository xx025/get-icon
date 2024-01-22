from setuptools import setup, find_packages

setup(
    name="get-icon",
    version="0.0.1",
    description="Obtain the favicon/icon or apple-touch-icon of a website with a very high success rate.",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "selenium",
        "setuptools",
        "python-magic",
        "python-magic-bin",
        "fake-useragent"
    ],
)
