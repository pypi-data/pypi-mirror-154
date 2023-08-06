# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_exe']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0b1,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['exe = poetry_plugin_exe:PoetryPluginExe']}

setup_kwargs = {
    'name': 'poetry-plugin-exe',
    'version': '0.0.1',
    'description': 'Poetry plugin to execute commands and/or scripts',
    'long_description': '# poetry-plugin-exe\nA plugin for poetry that allows script and command execution without including them in release.\n',
    'author': 'Christian Wiche',
    'author_email': 'cwichel@gmail.com',
    'maintainer': 'Christian Wiche',
    'maintainer_email': 'cwichel@gmail.com',
    'url': 'https://github.com/cwichel/poetry-plugin-exe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
