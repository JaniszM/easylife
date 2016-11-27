from setuptools import setup

setup(
    name='easylife',
    packages=['easylife'],  # this must be the same as the name above
    version='0.0.1',
    description='Group of scripts that makes your life easier.',
    author='Janiszewski Marcin',
    author_email='janiszewski.m.a@gmail.com',
    url='https://github.com/JaniszM/easylife',
    download_url='https://github.com/JaniszM/easylife/tarball/0.0.1',
    install_requires=["selenium==3.0.1",
                      "jsonschema==2.5.1"],
    keywords=['easy', 'life', 'shorthand', 'quick', 'script', 'tool', 'useful'],  # arbitrary keywords
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
    ],
    entry_points={
        'console_scripts': [
            'easylife = easylife.bank_transfers:main',
        ],
    },
    package_data={
        'easylife': ["user_data_schema.json"]
    }
)
