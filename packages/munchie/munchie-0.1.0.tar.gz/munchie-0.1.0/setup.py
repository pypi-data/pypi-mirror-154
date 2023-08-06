# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['munchie', 'munchie.filenom']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'munchie',
    'version': '0.1.0',
    'description': 'Compilation of commonly used functionality in personal projects',
    'long_description': None,
    'author': 'Anthony Gaetano',
    'author_email': 'adgaetano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
