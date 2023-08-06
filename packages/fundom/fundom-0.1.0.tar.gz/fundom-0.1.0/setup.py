# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fundom', 'fundom.pointfree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fundom',
    'version': '0.1.0',
    'description': 'Common simple python monads for more readable and maintainable pipeline-based code.',
    'long_description': None,
    'author': 'Ilya Katun',
    'author_email': 'katun.ilya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
