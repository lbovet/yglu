from setuptools import setup

setup(
    name='ylgu',
    version='0.1',
    description='YAML Glue',
    author='Laurent Bovet',
    author_email='laurent.bovet@windmaster.ch',
    packages=["yglu"],
    entry_points={
        "console_scripts": ["yglu=yglu.cli:main"]},
    install_requires=[
        "ruamel.yaml"
    ],
)