# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['proctools',
 'proctools.cli',
 'proctools.products',
 'proctools.products.pancam']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0',
 'numpy>=1.19.5,<2.0.0',
 'passthrough==0.3.2',
 'pds4-tools>=1.2,<2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.7.3,<4.0.0'],
 'cli': ['typer>=0.3.2,<0.5.0']}

setup_kwargs = {
    'name': 'proctools',
    'version': '0.2.1',
    'description': 'ProcTools - Common tools for (ExoMars) data product processing software',
    'long_description': None,
    'author': 'Ariel Ladegaard',
    'author_email': 'arl13@aber.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ExoMars-PanCam/proctools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
