# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.process', 'src.process.filters']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'opencv-python']

setup_kwargs = {
    'name': 'deepviewcore',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Miguel Martín',
    'author_email': 'alu0101209777@ull.edu.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
