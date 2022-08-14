from setuptools import setup, find_packages
import mosquito
import sys
import os

setup(
        name = 'mosquito',
        version = mosquito.__version__,
        description = 'simple multi purpose tools that do not readily exist in common python packages',
        url = 'https://github.com/sodiumnitrate/mosquito.git',
        author = 'Irem Altan',
        author_email = 'irem.altan@yale.edu',
        packages = find_packages(),
        install_requires = ['numpy'],
        python_requires = '>=3.6',
        )


