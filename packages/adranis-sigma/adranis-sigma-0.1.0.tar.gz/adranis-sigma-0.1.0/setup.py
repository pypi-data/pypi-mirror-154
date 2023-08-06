# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adranis_sigma', 'adranis_sigma.uq']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.8.2,<6.0.0',
 'scipy>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'adranis-sigma',
    'version': '0.1.0',
    'description': 'Firt release of the python binding of the Adranis Sigma API',
    'long_description': None,
    'author': 'Adranis GmbH',
    'author_email': 'contact@adranis.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
