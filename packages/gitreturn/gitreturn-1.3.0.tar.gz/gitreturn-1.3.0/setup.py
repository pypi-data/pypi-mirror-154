# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitreturn']

package_data = \
{'': ['*']}

install_requires = \
['inquirerpy>=0.3.3,<0.4.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['git_return = gitreturn.cli:run']}

setup_kwargs = {
    'name': 'gitreturn',
    'version': '1.3.0',
    'description': 'Script to return to staging.',
    'long_description': None,
    'author': 'blackboardd',
    'author_email': 'brightenqtompkins@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
