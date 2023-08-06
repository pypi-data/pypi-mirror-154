# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['binance_bigdata']

package_data = \
{'': ['*']}

install_requires = \
['python-binance>=1.0.16,<2.0.0', 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'binance-bigdata',
    'version': '0.1.0',
    'description': 'Study of crypto currencies in python.',
    'long_description': None,
    'author': 'Marc Partensky',
    'author_email': 'marc.partensky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
