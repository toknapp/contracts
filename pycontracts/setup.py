from setuptools import setup, find_packages

with open("../README.md", "r") as fh:
    long_description = fh.read()

# deps
with open('requirements.txt') as f:
    required = f.read().splitlines()

about = {}
with open("__pkginfo__.py") as f:
    exec(f.read(), about)    

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],    
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    url=about['__url__'],
    keywords="contracts blockchain upvest ethereum web3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=required,
)
