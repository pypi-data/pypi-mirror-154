# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ieee_patch']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'lxml>=4.9.0,<5.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['ieee-patch = ieee_patch.patch:main',
                     'xml-pretty-print = ieee_patch.xml_pretty_print:main']}

setup_kwargs = {
    'name': 'dcs-ms-word-ieee-patch',
    'version': '0.2.0',
    'description': 'Patch IEEE citation format in Microsoft Word docx documents',
    'long_description': None,
    'author': 'dotcs',
    'author_email': 'git@dotcs.me',
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
