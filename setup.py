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
    author='TommyStarK <Thomas Milox>',
    author_email='thomasmilox@gmail.com',
    description='Tool to build CLTV model or predict future sales for given data',
    long_description=open('README.md').read(),
    install_requires=requirements,
    include_package_data=True,
    url='https://github.com/TommyStarK/cltv-predict',
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
