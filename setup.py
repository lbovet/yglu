from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("yglu/__init__.py", "r") as fh:
    exec(fh.read())

setup(
    name='yglu',
    version=version,
    description='YAML glue for structural templating and processing',
    author='Laurent Bovet',
    author_email='laurent.bovet@windmaster.ch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yglu.io",
    project_urls={  
        'Documentation': 'https://github.com/lbovet/yglu/blob/master/README.md',
        'Bug Reports': 'https://github.com/lbovet/yglu/issues',
        'Source': 'https://github.com/lbovet/yglu'
    },    
    packages=["yglu"],
    entry_points={
        "console_scripts": ["yglu=yglu.cli:main"]
    },
    install_requires=[
        "ruamel.yaml>=0.16.5",
        "yaql>=1.1.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
