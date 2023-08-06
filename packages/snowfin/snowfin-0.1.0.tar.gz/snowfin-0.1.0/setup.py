# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowfin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snowfin',
    'version': '0.1.0',
    'description': 'An async discord http interactions framework built on top of Sanic.',
    'long_description': None,
    'author': 'kaj',
    'author_email': '40004347+KAJdev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
