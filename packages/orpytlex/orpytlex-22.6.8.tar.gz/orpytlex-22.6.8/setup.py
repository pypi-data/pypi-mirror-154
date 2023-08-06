# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['orpytlex', 'orpytlex.classes']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['orpytlex_downloader = orpytlex.main:main']}

setup_kwargs = {
    'name': 'orpytlex',
    'version': '22.6.8',
    'description': 'Simple project description - Our Python Tool Example',
    'long_description': '# OrPyTlEx README file',
    'author': 'Tadeusz Miszczyk',
    'author_email': 'tadeusz.miszczyk@server.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/8tm/orpytlex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
