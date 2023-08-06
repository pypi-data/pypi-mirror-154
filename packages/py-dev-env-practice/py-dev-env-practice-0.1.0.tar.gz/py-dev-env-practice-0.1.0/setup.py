# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_dev_env_practice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-dev-env-practice',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '1eedaegon',
    'author_email': 'd8726243@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
