# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'entest',
    'version': '0.1.6',
    'description': 'Write dependaent integration tests. See my pycon talk.',
    'long_description': None,
    'author': 'Peteris Ratnieks',
    'author_email': 'peteris.ratnieks@zealid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
