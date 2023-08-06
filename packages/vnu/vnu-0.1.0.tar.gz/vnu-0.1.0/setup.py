# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vnu']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['vnu = vnu.main:main']}

setup_kwargs = {
    'name': 'vnu',
    'version': '0.1.0',
    'description': 'A small utility to automate \\"uninstalling\\" Node from Volta',
    'long_description': '# VNU (Volta Node Uninstaller)\nVNU is a simple utility to simplify the task of removing (or "uninstalling") Node from [Volta](https://volta.sh/).\nVolta, as of June 2nd, 2022 is still missing this functionality.\n\n## Why?\nAt work we we\'re thinking about implementing `volta` instead of `n` and one of the pushback reasons we got to not implement it was the inability to remove unused Node versions.\n\nI took it upon myself to try and automate this seemingly trivial task. Enter VNU.\n\n## Usage\n`vnu -l` will list all available Node versions on Volta.\n\n`vnu -V VERSION` will uninstall `VERSION` or show matching versions based on regex, e.g.:\n```\n❯ vnu -V 10\nVNU (Volta Node Uninstaller)\nWe found the following versions for 10. Which one would you like to uninstall?\n1. 10.8.0\n2. 10.23.1\n3. 10.24.1\n0. Cancel\n```\n\n## Disclaimer\nI\'m not a programmer. I learn by doing and this is one of my small projects to help me do exactly that.\nWhat this means is - this project and the code within it might be ugly and could probably be implemented in a million of better ways. This is exactly why I am sharing this with you, the smart people of the internet.\n\n*I AM looking for feedback.* I do want to improve this little utility for everyone with your assistance.',
    'author': 'Paul Glushak',
    'author_email': 'paul@glushak.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hxii/vnu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
