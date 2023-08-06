# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysignald_async']

package_data = \
{'': ['*']}

install_requires = \
['aiosignald']

setup_kwargs = {
    'name': 'pysignald-async',
    'version': '0.2',
    'description': 'Python bindings for signald',
    'long_description': 'Signald python bindings\n=======================\n\nThis project has been moved and renamed `aiosignald <https://gitlab.com/nicocool84/aiosignald>`_',
    'author': 'Nicolas Cedilnik',
    'author_email': 'nicoco@nicoco.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nicocool84/pysignald-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
