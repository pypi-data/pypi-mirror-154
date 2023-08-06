# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 20:31:14 2022

@author: Guanhui Sun
"""

from setuptools import setup



setup(name='library_sun1',  # package name
      version='1.0.0', 
      description='this is my first package',
      author='Guanhui Sun',
      author_email='gs3725@nyu.edu',   
      packages = ["library_sun1"],
      install_requires=[],
      license='MIT License',
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ]
      )