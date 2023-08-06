from setuptools import setup

requires = [
    "lxml",
    "bs4",
    "mechanicalsoup",
    "cloudscraper",
]

setup(
    name='scrapinglib',
    version='0.2.1',
    author="suwmlee",
    author_email='suwmlee@gmail.com',
    url='https://github.com/Suwmlee/scrapinglib',
    packages=["scrapinglib"],
    package_dir={'scrapinglib': 'scrapinglib'},   
    install_requires=requires,
)
