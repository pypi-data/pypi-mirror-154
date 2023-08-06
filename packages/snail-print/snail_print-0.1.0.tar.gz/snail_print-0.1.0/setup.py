# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snail_print']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snail-print',
    'version': '0.1.0',
    'description': 'A print funtion that slowly shows the output in console in real time',
    'long_description': None,
    'author': 'Jose Antonio Castro',
    'author_email': 'jacastro18@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
