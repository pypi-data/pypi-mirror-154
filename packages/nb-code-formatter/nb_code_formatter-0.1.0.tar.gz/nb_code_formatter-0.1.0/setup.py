# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_code_formatter']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0', 'isort>=5.10.1,<6.0.0', 'nbformat>=5.4.0,<6.0.0']

entry_points = \
{'console_scripts': ['nbcodefmt = nb_code_formatter:main']}

setup_kwargs = {
    'name': 'nb-code-formatter',
    'version': '0.1.0',
    'description': 'code formatter for ipynb files',
    'long_description': 'nb-code-formatter\n=================\n\ncode formatter for ipynb files.',
    'author': 'driller',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drillan/nb-code-formatter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
