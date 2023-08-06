# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['senfoni']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'senfoni',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'rcmalli',
    'author_email': 'refikcanmalli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
