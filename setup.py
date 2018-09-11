# -*- coding: utf-8 -*-
from setuptools import find_packages
from cx_Freeze import setup, Executable

import cltv

# project requirements from pip
with open('requirements.txt') as requirement_file:
    requirements = requirement_file.read().splitlines()


setup(
    name='cltv',
    version=cltv.__version__,
    packages=find_packages(),
    author='AT Internet TeamDataScience',
    author_email='TeamDataScience@atinternet.com',
    description='AT Internet CLTV implementation',
    long_description=open('README.md').read(),
    install_requires=requirements,
    include_package_data=True,
    url='http://git.intraxiti.com/ML/CLTV',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'cltvd = cltv.cltv:main',
        ],
    },
    executables=[Executable('app.py')]
)
