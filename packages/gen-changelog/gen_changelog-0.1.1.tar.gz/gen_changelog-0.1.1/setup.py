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
    'version': '0.1.1',
    'description': 'A very simple script to generate a changelog from a repo with Conventional-Commits-compatible commit messages.',
    'long_description': 'gen_changelog\n=============\n\ngen_changelog is a very simple script that generates a changelog from a repository with\ncommit messages compatible with [Conventional\nCommits](https://www.conventionalcommits.org/). The main difference of this script from\n[gitchangelog](https://github.com/sarnold/gitchangelog) is that this script will\ngenerate sections from dates/months instead of git tags of versions.\n\n\nUsage\n-----\n\nJust run it in the root of your repository:\n\n```bash\n$ ./gen_changelog "Your project\'s name"\n```\n\nYou\'re done.\n\n\nCustomization\n-------------\n\nYou can customize the sections you want in the changelog by passing the `--categories`\nparameter:\n\n```bash\n$ ./gen_changelog --categories "add:Added|rem:Removed|chg:Changed|cs:CS:GO stuff"\n```\n\n\nWith pre-commit\n---------------\n\nTo use this with pre-commit, add this to your `.pre-commit-config.yaml`:\n\n```yaml\n- repo: https://gitlab.com/stavros/gen_changelog.git\n  rev: ccc6fa1dbe1a937c9b729e356b5fd91bf9d59ca4\n  hooks:\n  - id: gen-changelog\n    stages: [commit]\n```\n',
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
