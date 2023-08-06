# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peter_parquet']

package_data = \
{'': ['*']}

install_requires = \
['pyarrow[all]>=8.0.0,<9.0.0',
 'rich[all]>=12.4.4,<13.0.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['peter-parquet = peter_parquet.main:app']}

setup_kwargs = {
    'name': 'peter-parquet',
    'version': '0.3.0',
    'description': '',
    'long_description': '# Peter Parquet\nQuickly inspect parquet file in command line\n\n# Where to get it\nThe source coid is currently hosted on Github at:\nBinary installers for the latest version are available at the repo\n\n```bash\npip install peter-parquet\n```\n\n# Usage\n`peter-parquet --help` return all commands available\n\n# Non Bash users\nIf you are a non Bash user, notice that Python package executables are installed to ~/.local/bin. So, make sure to add this entry to your PATH variable.\n\n',
    'author': 'sjlva',
    'author_email': 'rafaelsilva@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjlva/peter-parquet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
