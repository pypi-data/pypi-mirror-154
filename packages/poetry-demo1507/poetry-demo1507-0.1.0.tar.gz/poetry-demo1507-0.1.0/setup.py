# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo1507']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['publish = poetry_demo.main:add']}

setup_kwargs = {
    'name': 'poetry-demo1507',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sarang Mulewa',
    'author_email': 'sarangmulewa1us@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
