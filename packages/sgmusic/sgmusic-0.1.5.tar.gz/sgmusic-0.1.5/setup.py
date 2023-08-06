# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sgmusic']

package_data = \
{'': ['*']}

install_requires = \
['sympy>=1.10,<2.0']

setup_kwargs = {
    'name': 'sgmusic',
    'version': '0.1.5',
    'description': '',
    'long_description': '<div align="center">\n  \n  [![Package Tests](https://github.com/SG60/sgmusic/actions/workflows/tests.yml/badge.svg)](https://github.com/SG60/sgmusic/actions/workflows/tests.yml)\n  [![codecov](https://codecov.io/gh/SG60/sgmusic/branch/master/graph/badge.svg?token=BXYBVS5HF9)](https://codecov.io/gh/SG60/sgmusic)\n  [![Code Style](https://github.com/SG60/sgmusic/actions/workflows/code-style.yml/badge.svg)](https://github.com/SG60/sgmusic/actions/workflows/code-style.yml)\n  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n  # sgmusic Python Library\n\n</div>\n\n\n\nUsing poetry, mypy, isort, black.\n\nPytest for testing.\n\n[commitizen](https://github.com/commitizen-tools/commitizen) for commit messages and semver (use `cz c` for commits, `cz bump` to update version, `git push --tags` to update tags on Github)\n',
    'author': 'Sam Greening',
    'author_email': 'samjg60@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SG60/sgmusic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
