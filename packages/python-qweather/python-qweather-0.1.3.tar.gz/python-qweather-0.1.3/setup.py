# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_qweather']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-qweather',
    'version': '0.1.3',
    'description': 'Python API wrapper for https://qweather.com',
    'long_description': '# python-qweather\n\nPython API wrapper for [和风天气](https://qweather.com)。',
    'author': 'dofine',
    'author_email': 'dofine@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
