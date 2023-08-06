# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deap_er', 'deap_er.tools', 'deap_er.tools.hyper_volume']

package_data = \
{'': ['*'], 'deap_er.tools': ['hyper_volume/c_ext/*']}

install_requires = \
['numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'deap-er',
    'version': '0.2.0',
    'description': 'DEAP port to Python 3.10',
    'long_description': None,
    'author': 'Mattias Aabmets',
    'author_email': 'mattias.aabmets@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
