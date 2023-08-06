# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['browserbook', 'browserbook.tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'browserbook',
    'version': '0.1.7',
    'description': 'A web browser backend. Gets all data needed from a url. Multiple sessions at once is possible',
    'long_description': '',
    'author': 'DragonHunter',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thatrandomperson5/BrowserBook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
