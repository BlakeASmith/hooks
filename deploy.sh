#!/bin/sh
rm -r dist
python setup.py sdist bdist_wheel
twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*
