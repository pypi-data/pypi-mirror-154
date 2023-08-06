# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sco1_misc']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0', 'numpy>=1.22,<2.0', 'pandas>=1.4,<2.0']

entry_points = \
{'console_scripts': ['csvdatetrim = misc.csv_date_trim:trim_cli']}

setup_kwargs = {
    'name': 'sco1-misc',
    'version': '0.1.0',
    'description': 'A collection of miscellaneous helpers.',
    'long_description': '# misc\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://vscode.dev/github.com/sco1/py-template)\n\nA collection of miscellaneous helpers.\n',
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
