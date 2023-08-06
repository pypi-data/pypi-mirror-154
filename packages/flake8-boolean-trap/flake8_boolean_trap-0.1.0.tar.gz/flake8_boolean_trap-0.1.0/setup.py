# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['flake8_boolean_trap']
install_requires = \
['flake8>=4.0.1,<5.0.0']

entry_points = \
{'flake8.extension': ['FBT = flake8_boolean_trap:Plugin']}

setup_kwargs = {
    'name': 'flake8-boolean-trap',
    'version': '0.1.0',
    'description': 'flake8 plugin which forbids boolean positional arguments',
    'long_description': '# Flake8 Boolean Trap\n\nA flake8 plugin to detect boolean traps.\n\n## Setup\n\n### prerequisites\n\n* python>=3.7\n* flake8 >=4\n\n### install\n\n```console\n$ pip install flake8_boolean_trap\n```\n\n## Usage\n\nJust run `flake8` as you normally would.\n\n## Lint Codes\n\n| Code.  | Description                                   |\n| ------ | --------------------------------------------- |\n| FBT001 | Boolean positional arg in function definition |\n| FBT002 | Boolean default value in function definition  |\n| FBT003 | Boolean positional value in function call     |\n',
    'author': 'Pablo Woolvett',
    'author_email': 'github@devx.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pwoolvett.github.io/flake8_boolean_trap',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
