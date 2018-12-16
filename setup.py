import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="thesaurus",
    version="0.2.2",
    author="Robert Dominguez",
    author_email="robert@robertism.com",
    description="Access synonym and antonym data from thesaurus.com in style.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Manwholikespie/thesaurus",
    entry_points={
        'console_scripts': ['thesaurus-dot-com=thesaurus.cli:main']
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.13.0',
        'beautifulsoup4>=4.6.0',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    )
)