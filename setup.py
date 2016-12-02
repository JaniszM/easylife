# coding=utf-8

from os import path
from setuptools import setup

from easylife import VERSION

here = path.abspath(path.dirname(__file__))

# def _readme():
#     """
#     Get the long description from the relevant file.
#     """
#     with open(path.join(here, 'README.md')) as f:
#         return f.read()


setup(
    name='easylife',
    packages=['easylife', 'easylife/transfers'],
    version=VERSION,
    description='Group of useful scripts and tools that makes your life easier by doing things for you.'
                ' Automates same things you can do every day.',
    # long_description=_readme(),
    author='Janiszewski Marcin',
    author_email='janiszewski.m.a@gmail.com',
    license='MIT',
    url='https://github.com/JaniszM/easylife',
    download_url='https://github.com/JaniszM/easylife/tarball/{0}'.format(VERSION),
    install_requires=["selenium==3.0.1",
                      "jsonschema==2.5.1",
                      "requests==2.12.3"],
    keywords=['easy', 'life', 'shorthand', 'quick', 'script', 'tool', 'useful',
              'bill', 'transfer', 'bank'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Home Automation',
    ],
    entry_points={
        'console_scripts': [
            'easylife = easylife.run_tools:main',
        ],
    },
    include_package_data=True
)
