# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen_changelog']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0']

entry_points = \
{'console_scripts': ['gen_changelog = gen_changelog.cli:cli']}

setup_kwargs = {
    'name': 'gen-changelog',
    'version': '0.1.0',
    'description': 'A very simple script to generate a changelog from a repo with Conventional-Commits-compatible commit messages.',
    'long_description': None,
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
