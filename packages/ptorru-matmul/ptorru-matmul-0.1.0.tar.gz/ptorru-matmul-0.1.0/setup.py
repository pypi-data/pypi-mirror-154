# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptorru_matmul']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'ptorru-matmul',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pedro Torruella',
    'author_email': 'ptorru14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
