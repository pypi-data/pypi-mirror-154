# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obito']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['obito = Obito.downloader:main']}

setup_kwargs = {
    'name': 'obito',
    'version': '0.1.0',
    'description': 'A URL file downloader that can download multiple files concurrently over internet.',
    'long_description': "![logo](https://cdn.discordapp.com/attachments/983572908553150484/984755765388648458/logo.png)\n\n### **[Obito](https://naruto.fandom.com/wiki/Obito_Uchiha)** is a URL file downloader which can download multiple files concurrently over internet.\n\n- **What's different?**\n    - [x] Downloads multiple files through single command.\n    - [x] Downloads files concurrently.\n    - [ ] Support for large files.\n\n## USAGE\n![usage](https://user-images.githubusercontent.com/76993204/173182137-1499286b-bfed-40d9-889e-12ac9ff5a352.svg)\n\n## Installation\n#### ***PyPi***\n```bash\npip install Obito\n```\n</br>\n\n#### ***Manual Installation***\n**Note:** You will need [Poetry](https://python-poetry.org/) for manual installation.\n```bash\npip install poetry\n```\n</br>\n\n1. Download or clone the repository.\n```bash\ngit clone https://github.com/777advait/Obito\n```\n\n2. Install the project by running the following command in the root of the directory.\n```bash\npoetry install\n```\n\n## Examples\n#### 1. Downloading Github API and Python concurrency docs\n![example_1](https://user-images.githubusercontent.com/76993204/173182602-6ef5f13d-b1a7-4d52-9bf5-467fbf06d19e.gif)\n</br>\n\n#### 2. Downloading [Rust](https://rust-lang.org).\n![example_2](https://user-images.githubusercontent.com/76993204/173183043-9d963973-be4f-48bd-b82e-ae1e4282d10d.gif)",
    'author': '777advait',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/777advait/Obito',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
