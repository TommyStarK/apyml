# -*- coding: utf-8 -*-
from setuptools import find_packages
from cx_Freeze import setup, Executable

import apyml

install_requires = [    
    'cx_Freeze'
    'pandas'
]

setup(
    name='apyml',
    version=apyml.__version__,
    packages=find_packages(),
    author=apyml.__author__,
    author_email='thomasmilox@gmail.com',
    description='Apyml - a Machine learning model building tool for humans.',
    long_description=open('README.md').read(),
    install_requires=install_requires,
    include_package_data=True,
    url='https://github.com/TommyStarK/apyml',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'apyml = apyml.__main__:main',
        ],
    },
    executables=[Executable('app.py')]
)
