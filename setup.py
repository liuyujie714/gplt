#!/usr/bin/python3
# coding: utf-8

from setuptools import setup, find_packages

# Always update program version
__version__ = '0.1.12.8'

# Description
long_doc = ""
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_doc = f.read()
except:
    pass

setup(
    name='gplt',
    version=__version__,
    description='A program for plotting gromacs output data', 
    long_description=long_doc,
    long_description_content_type='text/markdown',
    license='GPL',
    author='Yujie Liu',
    author_email='',
    python_requires='>=3.8',
    install_requires=['typing_extensions', 'numpy', 'matplotlib', 'colorama', 'pandas', 'openpyxl'],
    exclude=['setup.py'],
    packages=find_packages(include=['gplt', 'gplt.*']),
    entry_points={"console_scripts": ["gplt = gplt.gplt:gplt_command"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Science/Research",
    ]
)
