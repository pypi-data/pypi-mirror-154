# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['browserbook', 'browserbook.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'browserbook',
    'version': '0.1.3',
    'description': 'A web browser backend. Gets all data needed from a url. Multiple sessions at once is possible',
    'long_description': None,
    'author': 'DragonHunter',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
