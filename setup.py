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
    packages=['easylife', 'easylife/transfers', 'easylife/photo_organizer'],
    version=VERSION,
    description='Group of useful scripts and tools that makes your life easier by doing things for you.'
                ' Automates same things you can do every day.',
    long_description='https://github.com/JaniszM/easylife/blob/master/README.md',
    author='Janiszewski Marcin',
    author_email='janiszewski.m.a@gmail.com',
    license='MIT',
    url='https://github.com/JaniszM/easylife',
    download_url='https://github.com/JaniszM/easylife/tarball/{0}'.format(VERSION),
    install_requires=["selenium==3.4.3",
                      "jsonschema==2.5.1",
                      "requests==2.12.3",
                      "exifread==2.1.2"],
    keywords=['easy', 'life', 'tool', 'useful', 'automation', 'shorthand'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.0',
        'Development Status :: 5 - Production/Stable',
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
