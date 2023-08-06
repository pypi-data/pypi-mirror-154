# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpge', 'cpge.graph']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0', 'matplotlib>=3.5.2,<4.0.0', 'numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'cpge',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Quentin Fortier',
    'author_email': 'qpfortier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
