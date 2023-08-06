# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt',
 'dlt.cli',
 'dlt.common',
 'dlt.common.configuration',
 'dlt.common.storages',
 'dlt.dbt_runner',
 'dlt.extractors',
 'dlt.extractors.generator',
 'dlt.loaders',
 'dlt.loaders.dummy',
 'dlt.loaders.gcp',
 'dlt.loaders.redshift',
 'dlt.pipeline',
 'dlt.unpacker',
 'examples',
 'examples.schemas',
 'examples.sources']

package_data = \
{'': ['*'], 'examples': ['data/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'hexbytes>=0.2.2,<0.3.0',
 'json-logging==1.4.1rc0',
 'jsonlines>=2.0.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'requests>=2.26.0,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.4.3,<2.0.0',
 'simplejson>=3.17.5,<4.0.0']

extras_require = \
{'dbt': ['GitPython>=3.1.26,<4.0.0',
         'dbt-core==1.0.6',
         'dbt-redshift==1.0.1',
         'dbt-bigquery==1.0.0'],
 'gcp': ['grpcio==1.43.0', 'google-cloud-bigquery>=2.26.0,<3.0.0'],
 'postgres': ['psycopg2-binary>=2.9.1,<3.0.0'],
 'redshift': ['psycopg2-binary>=2.9.1,<3.0.0']}

entry_points = \
{'console_scripts': ['dlt = dlt.cli.dlt:main']}

setup_kwargs = {
    'name': 'python-dlt',
    'version': '0.1.0rc1',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': 'Follow this quick guide to implement DLT in your project\n\n## Simple loading of one row:\n\n### Install DLT\nDLT is available in PyPi and can be installed with `pip install python-dlt`. Support for target warehouses is provided in extra packages:\n\n`pip install python-dlt[redshift]` for Redshift\n\n`pip install python-dlt[gcp]` for BigQuery\n\n### Create a target credential\n```\ncredential = {\'type\':\'redshift\',\n                \'host\': \'123.456.789.101\'\n                \'port\': \'5439\'\n                \'user\': \'loader\'\n                \'password\': \'dolphins\'\n\n                }\n\n\n```\n\n### Initialise the loader with your credentials and load one json row\n```\nimport dlt\n\nloader = dlt(credential)\n\njson_row = "{"name":"Gabe", "age":30}"\n\ntable_name = \'users\'\n\nloader.load(table_name, json_row)\n\n```\n\n## Loading a nested json object\n\n```\nimport dlt\n\nloader = dlt(credential)\n\njson_row = "{"name":"Gabe", "age":30, "id":456, "children":[{"name": "Bill", "id": 625},\n                                                            {"name": "Cill", "id": 666},\n                                                            {"name": "Dill", "id": 777}\n                                                            ]\n            }"\n\n\ntable_name = \'users\'\n\n\n#unpack the nested json. To be able to re-pack it, we create the parent - child join keys via row / parent row hashes.\n\nrows = loader.utils.unpack(table_name, json_row)\n\n# rows are a generator that outputs the parent or child table name and the data row such as:\n\n#("users", "{"name":"Gabe", "age":30, "id":456, "row_hash":"parent_row_md5"}")\n#("users__children", "{"name":"Bill", "id":625, "parent_row_hash":"parent_row_md5", "row_hash":"child1_row_md5"}")\n#("users__children", "{"name":"Cill", "id":666, "parent_row_hash":"parent_row_md5", "row_hash":"child2_row_md5"}")\n#("users__children", "{"name":"Dill", "id":777, "parent_row_hash":"parent_row_md5", "row_hash":"child3_row_md5"}")\n\n\n#loading the tables users, and users__children\nfor table, row in rows:\n    loader.load(table_name, row)\n\n\n#to recreate the original structure\nselect users.*, users__children.*\nfrom users\nleft join users__children\n    on users.row_hash = users__children.parent_row_hash\n```\n',
    'author': 'ScaleVector',
    'author_email': 'services@scalevector.ai',
    'maintainer': 'Marcin Rudolf',
    'maintainer_email': 'marcin@scalevector.ai',
    'url': 'https://github.com/scale-vector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
