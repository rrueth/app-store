import codecs
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='app_store',
    version='1.0.1',
    description="Utilities for interacting with Apple's iTunes App Store",
    long_description=long_description,
    url='https://github.com/rrueth/app-store',
    license='MIT',
    author='Ryan Rueth',
    author_email='rrueth@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="iTunes AppStore",
    packages=find_packages(exclude=['tests*']),
    install_requires=["requests"],
)