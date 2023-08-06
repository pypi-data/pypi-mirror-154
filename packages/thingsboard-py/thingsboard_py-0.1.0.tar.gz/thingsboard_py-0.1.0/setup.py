# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingsboard_py']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'thingsboard-py',
    'version': '0.1.0',
    'description': 'Python client for ThingsBoard',
    'long_description': None,
    'author': 'Parham Alvani',
    'author_email': 'parham.alvani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
