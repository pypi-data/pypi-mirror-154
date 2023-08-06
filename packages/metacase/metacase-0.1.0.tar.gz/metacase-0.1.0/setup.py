# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metacase',
 'metacase.adapters',
 'metacase.adapters.polarion',
 'metacase.adapters.polarion.args',
 'metacase.adapters.polarion.utils',
 'metacase.args',
 'metacase.connectors',
 'metacase.connectors.jira',
 'metacase.schema']

package_data = \
{'': ['*'],
 'metacase.schema': ['.fmf/*',
                     'adapter/*',
                     'adapter/polarion/*',
                     'defects/*',
                     'requirements/*',
                     'testsuite/*']}

install_requires = \
['fmf>=1.1.0,<2.0.0',
 'jira>=3.2.0,<4.0.0',
 'requests>=2.28.0,<3.0.0',
 'urllib3>=1.26.9,<2.0.0']

extras_require = \
{'docs': ['myst-parser>=0.12.10,<0.13.0',
          'sphinx>=3.5.4,<4.0.0',
          'sphinx-autobuild>=2020.9.1,<2021.0.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0']}

entry_points = \
{'console_scripts': ['metacase = metacase.metacase:main']}

setup_kwargs = {
    'name': 'metacase',
    'version': '0.1.0',
    'description': 'MetaCase is test case exporter tool based on FMF (Flexible Metadata Format) .',
    'long_description': '# MetaCase\n\nUniversal test case metadata exporter tool.\n\nThis tool can be used to convert and export Test Cases defined\nusing an [FMF](https://fmf.readthedocs.io/en/latest/) tree.\n\nThe test cases must be defined according to an [internal schema](./metacase/schema)\nand the MetaCase can parse them and invoke a selected adapter to convert / export the\nselect test cases into an external ALM related tool.\n\nFormat for defining the test case is YAML. [Example here](./examples)\n\n## Pre-requisites\n\n* Python 3.9+\n\n[//]: # (TODO: Readme installation)\n## Installation\n\n```\npip install metacase\n```\n\nor\n\n```\npip install -e git+https://github.com/enkeys/metacase.git\n```\n\n## Usage\n\nFor basic usage information, use:\n\n```\nmetacase --help\n```\n\n## Adapters\n\nThis tool provides a generic `metacase.adapter.Adapter` interface that can be implemented\nfor new external ALM related tools.\n\n### Polarion ALM\n\nAdapter (early stage) that can export a test case defined using FMF (compliant with internal FMF Test Case metadata\nschema) into Polarion test case importer API.\n\nFor help, use:\n\n```\nmetacase polarion --help\n```\n\n## Connectors\n\nConnector are helpers that can obtain information from external sources such as issue tracker, source repository, etc.\n\n## Contributors\n\nhttps://github.com/enkeys/metacase/graphs/contributors\n\n## Acknowledgments\n\n* [fmf](https://fmf.readthedocs.io/en/latest/) - Flexible Metadata Format - Makes it easier to document\nand query for your metadata.\n',
    'author': 'Fernando Giorgetti',
    'author_email': 'fgiorget@redhat.com',
    'maintainer': 'Dominik Lenoch',
    'maintainer_email': 'dlenoch@redhat.com',
    'url': 'https://github.com/enkeys/metacase/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
