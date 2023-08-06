# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['please']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.6,<6.0',
 'autopep8>=1.6.0,<2.0.0',
 'ics>=0.7,<0.8',
 'imgrender>=0.0.4,<0.0.5',
 'pyfiglet>=0.8.post1,<0.9',
 'python-jsonstore>=1.3.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['please = please.please:main']}

setup_kwargs = {
    'name': 'please-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nayam Amarshe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
