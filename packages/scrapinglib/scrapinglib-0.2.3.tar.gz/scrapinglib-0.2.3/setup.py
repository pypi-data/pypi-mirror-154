from setuptools import setup

requires = [
    "lxml",
    "mechanicalsoup",
    "cloudscraper",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='scrapinglib',
    version='0.2.3',
    author="suwmlee",
    author_email='suwmlee@gmail.com',
    url='https://github.com/Suwmlee/scrapinglib',
    packages=["scrapinglib"],
    package_dir={'scrapinglib': 'scrapinglib'},   
    install_requires=requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/Suwmlee/scrapinglib/issues",
        "Source": "https://github.com/Suwmlee/scrapinglib",
    },
)
