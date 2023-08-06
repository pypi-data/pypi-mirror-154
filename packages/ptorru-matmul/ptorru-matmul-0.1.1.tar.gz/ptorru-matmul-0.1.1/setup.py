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
    'version': '0.1.1',
    'description': 'Learning how to publish in PyPi through a generic implementation of matrix multiplication',
    'long_description': '# ptorru-matmul\n\nLearning about pipy, distributing a simple matrix multiply example\n\n# Dependencies\n\n[Poetry](https://python-poetry.org), [installation instructions](https://python-poetry.org/docs/).\n\n# After clonning\n\n```bash\ncd ptorru-matmul\npoetry init\n```\n\n# Running tests\n\n```bash\npoetry run pytest tests/\n```\n\n# Publishing\n\n## Setup PyPI token\n\n```bash\npoetry config pypi-token.pypi <TOKEN>\n```\n\n## Build and Publish\n\n```bash\npoetry build\npoetry publish\n```\n\n# References\n\nConsulted these resources:\n\n- [Utpal Kumar, The easiest way to publish a python package on PyPI using Poetry](https://www.earthinversion.com/utilities/easiest-way-to-publish-a-python-package-using-poetry/)\n',
    'author': 'Pedro Torruella',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ptorru/ptorru-matmul',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
