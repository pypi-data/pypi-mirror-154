# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sco1_misc']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0']

entry_points = \
{'console_scripts': ['csvdatetrim = sco1_misc.csv_date_trim:trim_cli']}

setup_kwargs = {
    'name': 'sco1-misc',
    'version': '0.1.1',
    'description': 'A collection of miscellaneous helpers.',
    'long_description': '# misc\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-misc)](https://pypi.org/project/sco1-misc/)\n[![PyPI](https://img.shields.io/pypi/v/sco1-misc)](https://pypi.org/project/sco1-misc/)\n[![PyPI - License](https://img.shields.io/pypi/l/sco1-misc?color=magenta)](https://github.com/sco1/sco1-misc/blob/main/LICENSE)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/sco1-misc/main.svg)](https://results.pre-commit.ci/latest/github/sco1/sco1-misc/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://vscode.dev/github.com/sco1/sco1-misc)\n\nA collection of miscellaneous helpers.\n\n## The Help\n### `sco1_misc.prompts`\nHelper wrappers for [`Tkinter`\'s selection dialogs](https://docs.python.org/3/library/dialog.html)\n\n  * `prompt_for_file(title: str, start_dir: pathlib.Path, multiple: bool, filetypes: list[tuple[str, str]])`\n  * `prompt_for_dir(title: str, start_dir: pathlib.Path)`\n\n### `csvdatetrim`\nA CLI tool for date windowing CSV log files\n\n**NOTE:** The following assumptions are made about the input CSV file:\n  * The CSV file contains a column named `"Time"`, with timestamps formatted as `MM/DD/YYYY HH:MM:SS` \n  * The CSV file ends on the same date as the specified date filter\n\n#### Input Parameters\n| Parameter        | Description                           | Type         | Default                         |\n|------------------|---------------------------------------|--------------|---------------------------------|\n| `--log-filepath` | Path to log file to trim.             | `Path\\|None` | GUI Prompt                      |\n| `--test_date`    | Trim date selection, as `YYYY-MM-DD`. | `str`        | Today\'s date                    |\n| `--out-filename` | Output filename.<sup>1,2,3</sup>      | `str\\|None`  | `<in_filename>_<test_date>.csv` |\n\n1. Output file is saved to the parent directory of `--log-filepath`\n2. Trimming will be aborted if `--out-filename` matches `--log-filepath`\n3. Any existing data will be discarded\n\n## Contributing\n### Development Environment\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies. With your fork cloned to your local machine, you can install the project and its dependencies to create a development environment using:\n\n```bash\n$ poetry install\n```\n\nA [pre-commit](https://pre-commit.com) configuration is also provided to create a pre-commit hook so linting errors aren\'t committed:\n\n```bash\n$ pre-commit install\n```',
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
