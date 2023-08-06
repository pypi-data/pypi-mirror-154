# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twts']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0', 'tweepy>=4.10.0,<5.0.0']

entry_points = \
{'console_scripts': ['twts = twts.stream:cli']}

setup_kwargs = {
    'name': 'twts',
    'version': '0.1.0',
    'description': 'stream tweets from the terminal',
    'long_description': None,
    'author': 'redraw',
    'author_email': 'redraw@sdf.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
