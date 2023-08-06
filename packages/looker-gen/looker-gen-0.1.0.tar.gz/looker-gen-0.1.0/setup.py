# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['looker_gen']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.2,<9.0.0',
 'lkml>=1.2.0,<2.0.0',
 'looker-sdk>=22.4.0,<23.0.0']

entry_points = \
{'console_scripts': ['gen = looker_gen.cli:gen',
                     'validate = looker_gen.cli:validate']}

setup_kwargs = {
    'name': 'looker-gen',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aaron Bannin',
    'author_email': 'aaronbannin@hotmail.com',
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
