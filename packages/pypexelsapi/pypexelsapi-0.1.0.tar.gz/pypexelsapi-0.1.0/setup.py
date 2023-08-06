# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypexelsapi', 'pypexelsapi.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypexelsapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'gl_epka',
    'author_email': 'nechaevgleb@inbox.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
