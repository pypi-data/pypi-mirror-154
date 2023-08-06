# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbce']
setup_kwargs = {
    'name': 'dbce',
    'version': '0.1.1',
    'description': 'DBCE - Discord Bot Creator Easy to use library for creating discord bots',
    'long_description': None,
    'author': 'peaky',
    'author_email': 'nerfinyt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
