# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylamine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylamine',
    'version': '0.1.0',
    'description': 'Python bindings for Calamine.',
    'long_description': None,
    'author': 'Chris Pryer',
    'author_email': 'cnpryer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
