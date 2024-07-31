#!/usr/bin/python3
# coding: utf-8

from setuptools import setup, find_packages

__version__ = '0.1.0'


setup(
    name='gplt',
    version=__version__,
    description='A program for plotting gromacs output data', 
    long_description='',
    long_description_content_type='text/markdown',
    license='GPL',
    author='Yujie Liu',
    author_email='',
    python_requires='>=3.8',
    install_requires=['typing_extensions', 'numpy'],
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
