# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['theotex']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['theotex = theotex.__main__:theotex']}

setup_kwargs = {
    'name': 'theotex',
    'version': '1.0.0',
    'description': 'A python package to get Bible verses from https://theotex.org',
    'long_description': '# Theotex\nA python module to get Bible verses from https://theotex.org\n',
    'author': 'numbergazing',
    'author_email': 'hello@numbergazing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
