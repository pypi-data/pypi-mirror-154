# -*- coding: utf-8 -*-
"""
Created on Fri June 6 3 16:40:44 2022

@author: danielgodinez
"""
from setuptools import setup, find_packages, Extension


setup(
    name="WeakLIA",
    version="0.1",
    author="Daniel Godines",
    author_email="danielgodinez123@gmail.com",
    description="Machine learning classifier for weak gravitational lensing",
    license='GPL-3.0',
    url = "https://github.com/Professor-G/StrongLIA",
    classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',	   
],
    packages=find_packages('.'),
    install_requires = ['numpy','scikit-learn', 'scikit-optimize', 'astropy','scipy','peakutils',
        'progress', 'matplotlib', 'missingpy', 'optuna', 'boruta', 'xgboost'],
    python_requires='>=3.7,<4',
    include_package_data=True,
    test_suite="nose.collector",
)
