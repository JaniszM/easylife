#!/usr/bin/env bash
echo "Pushing to test PyPi..."
python setup.py register -r pypitest
python setup.py sdist upload -r pypitest

echo "Pushing to PyPi..."
python setup.py register -r pypi
python setup.py sdist upload -r pypi
