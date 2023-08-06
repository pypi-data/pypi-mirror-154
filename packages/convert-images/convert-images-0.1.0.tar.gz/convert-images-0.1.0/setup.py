# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convert_images']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>7', 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['cim = convert_images:convert_images.main']}

setup_kwargs = {
    'name': 'convert-images',
    'version': '0.1.0',
    'description': 'Simple CLI to convert images to JPEG and PNG format',
    'long_description': '# Convert-images\n\n🚀 Simple CLI to convert images to JPEG and PNG format.\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n\n## Requirements\n- 🐍 [python>=3.6](https://www.python.org/downloads/)\n\n\n## ⬇️ Installation\n\n```sh\npip install convert-images\n```\n\n\n## ⌨️ Usage\n\n```\n➜ convert-images --help\n\n\n```\n\n\n## 📕 Examples\n',
    'author': 'Mohammad Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
