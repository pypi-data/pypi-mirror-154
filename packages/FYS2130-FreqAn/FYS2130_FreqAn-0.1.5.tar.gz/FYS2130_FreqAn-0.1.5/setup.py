from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.5'
DESCRITPION = 'Basic package for frequency analysis in FYS2130.'
LONG_DESCRITPION = open('README.txt').read() + '\n\n'

 # Setting up
setup(
    name='FYS2130_FreqAn',
    version=VERSION,
    author='Anton Brekke',
    author_email='anton.a@hotmail.no',
    description=DESCRITPION,
    long_description=LONG_DESCRITPION,
    packages=find_packages(),
    install_requires=[],
    classifiers=['']
)
