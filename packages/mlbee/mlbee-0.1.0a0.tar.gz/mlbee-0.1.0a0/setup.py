# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlbee']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['mlbee = mlbee.__main__:app']}

setup_kwargs = {
    'name': 'mlbee',
    'version': '0.1.0a0',
    'description': 'mlbee',
    'long_description': '# mlbee\n[![pytest](https://github.com/ffreemt/mlbee/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/mlbee/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/mlbee.svg)](https://badge.fury.io/py/mlbee)\n\nmlbee descr\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/mlbee\n# poetry add git+https://github.com/ffreemt/mlbee\n# git clone https://github.com/ffreemt/mlbee && cd mlbee\n```\n\n## Use it\n```python\nfrom mlbee import mlbee\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/mlbee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
