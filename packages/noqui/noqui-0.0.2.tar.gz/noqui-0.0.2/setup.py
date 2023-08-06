# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noqui']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noqui',
    'version': '0.0.2',
    'description': 'Implementation of unusual things',
    'long_description': None,
    'author': 'Roberto Alsina',
    'author_email': 'roberto.alsina@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
