# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['go_library',
 'go_library.amigo_solr',
 'go_library.datamodel',
 'go_library.implementations',
 'go_library.sqla',
 'go_library.utils']

package_data = \
{'': ['*']}

install_requires = \
['linkml-dataops>=0.1.0,<0.2.0',
 'linkml-runtime>=1.2.16,<2.0.0',
 'linkml-solr>=0.1.2,<0.2.0',
 'linkml>=1.2.13,<2.0.0',
 'oaklib>=0.1.21,<0.2.0',
 'sparqlfun>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['amigo = go_library.amigo_solr.amigo_cli:main',
                     'gocam = go_library.gocam_cli:main']}

setup_kwargs = {
    'name': 'go-library',
    'version': '0.1.0',
    'description': 'Enter description of your project here',
    'long_description': None,
    'author': 'Mark A. Miller',
    'author_email': 'mamillerpa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
