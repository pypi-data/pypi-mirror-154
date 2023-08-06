# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_graphql']

package_data = \
{'': ['*']}

install_requires = \
['cmem-cmempy>=21.11.5',
 'cmem-plugin-base==1.2.0a1',
 'gql[all]>=3.2.0,<4.0.0',
 'validators>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'cmem-plugin-graphql',
    'version': '0.0.1a1',
    'description': 'Executes a custom GraphQL query to a GraphQL endpoint and saves result to a JSON dataset.',
    'long_description': '# cmem-plugin-graphql\n\na CMEM Plugin to query GraphQL APIs and write the response to dataset of type JSON.\nIn the current release we are supporting only endpoints without authentication.\n',
    'author': 'Sai Praneeth M',
    'author_email': 'saipraneeth@aarth.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
