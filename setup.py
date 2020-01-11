from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ylgu-lbovet',
    version='0.1',
    description='YAML glue for structural templating and processing',
    author='Laurent Bovet',
    author_email='laurent.bovet@windmaster.ch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbovet/yglu",
    packages=["yglu"],
    entry_points={
        "console_scripts": ["yglu=yglu.cli:main"]
    },
    install_requires=[
        "ruamel.yaml",
        "yaql"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
