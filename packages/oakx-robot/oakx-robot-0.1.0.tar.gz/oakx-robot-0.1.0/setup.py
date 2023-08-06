# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oakx_robot']

package_data = \
{'': ['*']}

install_requires = \
['oaklib>=0.1.16,<0.2.0', 'py4j>=0.10.9,<0.11.0']

setup_kwargs = {
    'name': 'oakx-robot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'cmungall',
    'author_email': 'cjm@berkeleybop.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
