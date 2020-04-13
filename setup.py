import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

readme = (here / 'README.md').read_text()


setup(
        name='createhook',
        version="0.0.4",
        description='create hooks for functions',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/BlakeASmith/hooks',
        author='Blake Smith',
        classifiers=[
            "Programming Language :: Python :: 3"
        ],
        packages=find_packages(exclude = ['tests']),
)
