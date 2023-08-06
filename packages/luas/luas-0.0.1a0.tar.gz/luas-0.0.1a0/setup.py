# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['luas']
setup_kwargs = {
    'name': 'luas',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'Marco Rougeth',
    'author_email': 'rougeth@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
