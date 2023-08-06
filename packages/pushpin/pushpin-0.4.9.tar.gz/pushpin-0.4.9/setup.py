# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pushpin']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pushpin = pushpin:main']}

setup_kwargs = {
    'name': 'pushpin',
    'version': '0.4.9',
    'description': 'Git hooks for python 📌',
    'long_description': '<h1 align="center">pushpin</h1>\n\n<p align="center">\n<a href="https://raw.githubusercontent.com/nyanye/pushpin/main/docs/pushpin.png"><img src="https://raw.githubusercontent.com/nyanye/pushpin/main/docs/pushpin.png"></a><br>\n  <a href="https://github.com/nyanye/pushpin/actions/workflows/ci.yml"><img src="https://github.com/nyanye/pushpin/actions/workflows/ci.yml/badge.svg"/></a>\n  <a href="https://pypi.org/project/pushpin/"><img src="https://badge.fury.io/py/pushpin.svg" /></a>\n  <a href="https://pypi.org/project/pushpin/"><img src="https://img.shields.io/pypi/dm/ansicolortags.svg" /></a>\n</p>\n\n<p align="center">\nGit hooks for python 📌\n</p>\n<p align="center">\nPushpin improves your python commits and more.<br>\nYou can use it to run toolings like pytest, pylint, isort, black, etc<br>\nwhenever you commit or push. pushpin supports all Git hooks.<br>\nIt\'s basically <a href="https://typicode.github.io/husky/">husky</a> but for modern python toolings\n</p>\n\n\n# Install\n\n```bash\n# For poetry users\npoetry add -D pushpin\n\n# For traditional pip users\npip install pushpin\n```\n\n# Usage\n\n```bash\n# prepare your repo\npushpin install\n\n# add a hook\npushpin add .pushpin/pre-commit "pytest"\n```\n\n## Recommended Hooks\n\n```bash\n# pylint - strictly manage your code quality\npushpin add .pushpin/pre-commit "pylint --fail-under=8 ."\n\n# isort - sort your import orders\npushpin add .pushpin/pre-commit "isort ."\n\n# black - get some uncompromising styles\npushpin add .pushpin/pre-commit "black ."\n```\n\n# Used by\n\npushpin will be used by these awesome python projects.\n\n- list yours.\n\n',
    'author': 'Jung Daun',
    'author_email': 'iam@nyanye.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nyanye/pushpin',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2',
}


setup(**setup_kwargs)
