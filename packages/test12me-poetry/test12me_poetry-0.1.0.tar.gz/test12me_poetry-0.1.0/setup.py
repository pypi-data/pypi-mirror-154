# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test12me_poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test12me-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vikrant36',
    'author_email': '98794342+vikrant36@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
