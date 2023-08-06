# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configcafe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'configcafe',
    'version': '0.1.0',
    'description': 'Welcome to the config cafe.',
    'long_description': None,
    'author': "J 'Indi' Harrington",
    'author_email': 'indigoharrington@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
