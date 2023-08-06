# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mandeintegration', 'mandeintegration.config', 'mandeintegration.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'selenium>=4.2.0,<5.0.0',
 'webdriver-manager>=3.7.0,<4.0.0']

setup_kwargs = {
    'name': 'mandeintegration',
    'version': '0.1.1',
    'description': 'Mande Integration package',
    'long_description': None,
    'author': 'Sylvain Kadjo',
    'author_email': 'sylvain.kadjo@sejen.ci',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
