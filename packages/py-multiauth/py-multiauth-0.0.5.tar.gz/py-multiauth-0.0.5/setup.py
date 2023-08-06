# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiauth',
 'multiauth.providers',
 'multiauth.types',
 'multiauth.types.providers']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.0.1,<2.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'graphql-core>=3.2.1,<4.0.0',
 'pycognito>=2022.5.0,<2023.0.0',
 'pydash>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'py-multiauth',
    'version': '0.0.5',
    'description': 'Python package to interact with multiple authentication services',
    'long_description': '# py-multiauth\n',
    'author': 'Escape Technologies SAS',
    'author_email': 'ping@escape.tech',
    'maintainer': 'Antoine Carossio',
    'maintainer_email': 'antoine@escape.tech',
    'url': 'https://escape.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
