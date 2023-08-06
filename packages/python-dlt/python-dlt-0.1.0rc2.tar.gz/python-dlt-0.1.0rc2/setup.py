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
    'version': '0.1.0rc2',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': 'Follow this quick guide to implement DLT in your project\n\n## Simple loading of two rows:\n\n### Install DLT\nDLT is available in PyPi and can be installed with `pip install python-dlt`. Support for target warehouses is provided in extra packages:\n\n`pip install python-dlt[redshift]` for Redshift\n\n`pip install python-dlt[gcp]` for BigQuery\n\n\n### 1. Configuraton: name your schema, table, pass credentials\n\n```\n\nfrom dlt.pipeline import Pipeline, PostgresPipelineCredentials\n\nschema_prefix = \'demo_\'\nschema_name = \'example\'\nparent_table = \'my_json_doc\'\n\n# Credentials for Redshift or Bigquery\n\n# Redshift: you can pass password as last parameter or via PG_PASSWORD env variable.\n# credential = PostgresPipelineCredentials("redshift", "dbname", "schemaname", "username", "3.73.90.3", "dolphins")\n\n# Bigquery:\ngcp_credential_json_file_path = "scalevector-1235ac340b0b.json"\ncredential = Pipeline.load_gcp_credentials(gcp_credential_json_file_path, schema_prefix)\n\n# optionally save and reuse schema\n# schema_file_path = "examples/schemas/quickstart.yml"\n\n```\n\n### 2. Create a pipeline\n```\n\npipeline = Pipeline(schema_name)\npipeline.create_pipeline(credential)\n\n# Optionally uncomment to re-use a schema\n# schema = Pipeline.load_schema_from_file(schema_file_path)\n# pipeline.create_pipeline(credential, schema=schema)\n\n```\n\n### 3. Pass the data to the pipeline and give it a table name.\n```\n\nrows = [{"name":"Ana", "age":30, "id":456, "children":[{"name": "Bill", "id": 625},\n                                                       {"name": "Elli", "id": 591}\n                                                      ]},\n\n        {"name":"Bob", "age":30, "id":455, "children":[{"name": "Bill", "id": 625},\n                                                       {"name": "Dave", "id": 621}\n                                                      ]}\n       ]\n\npipeline.extract(iter(rows), table_name=parent_table)\n\n# Optionally the pipeline to un-nest the json into a relational structure\npipeline.unpack()\n\n# Optionally save the schema for manual edits/future use.\n# schema = pipeline.get_default_schema()\n# schema_yaml = schema.as_yaml()\n# f = open(data_schema_file_path, "a")\n# f.write(schema_yaml)\n# f.close()\n\n```\n\n### 4. Load\n\n```\npipeline.load()\n\n```\n\n### 5. Error capture - print, raise or handle.\n\n```\n# now enumerate all complete loads to check if we have any failed packages\n# complete but failed job will not raise any exceptions\ncompleted_loads = pipeline.list_completed_loads()\n# print(completed_loads)\nfor load_id in completed_loads:\n    print(f"Checking failed jobs in {load_id}")\n    for job, failed_message in pipeline.list_failed_jobs(load_id):\n        print(f"JOB: {job}\\nMSG: {failed_message}")\n\n```\n### 6. Use your data\n\n\nTables created:\n```\n SELECT *  FROM `scalevector.demo__example.my_json_doc`\nRESULT:\n{  "name": "Ana",  "age": "30",  "id": "456",  "_load_id": "1654787700.406905",  "_record_hash": "5b018c1ba3364279a0ca1a231fbd8d90"}\n{  "name": "Bob",  "age": "30",  "id": "455",  "_load_id": "1654787700.406905",  "_record_hash": "afc8506472a14a529bf3e6ebba3e0a9e"}\n\n\n SELECT * FROM `scalevector.demo__example.my_json_doc__children` LIMIT 1000\nRESULT:\n{  "name": "Bill",  "id": "625",  "_parent_hash": "5b018c1ba3364279a0ca1a231fbd8d90",  "_pos": "0",  "_root_hash": "5b018c1ba3364279a0ca1a231fbd8d90",  "_record_hash": "7993452627a98814cc7091f2c51faf5c"}\n{  "name": "Bill",  "id": "625",  "_parent_hash": "afc8506472a14a529bf3e6ebba3e0a9e",  "_pos": "0",  "_root_hash": "afc8506472a14a529bf3e6ebba3e0a9e",  "_record_hash": "9a2fd144227e70e3aa09467e2358f934"}\n{  "name": "Dave",  "id": "621",  "_parent_hash": "afc8506472a14a529bf3e6ebba3e0a9e",  "_pos": "1",  "_root_hash": "afc8506472a14a529bf3e6ebba3e0a9e",  "_record_hash": "28002ed6792470ea8caf2d6b6393b4f9"}\n{  "name": "Elli",  "id": "591",  "_parent_hash": "5b018c1ba3364279a0ca1a231fbd8d90",  "_pos": "1",  "_root_hash": "5b018c1ba3364279a0ca1a231fbd8d90",  "_record_hash": "d18172353fba1a492c739a7789a786cf"}\n\n```\nJoin your data via recursively created join keys.\n```\n select p.name, p.age, p.id as parent_id,\n        c.name as child_name, c.id as child_id, c._pos as child_order_in_list\n from `scalevector.demo__example.my_json_doc` as p\n left join `scalevector.demo__example.my_json_doc__children`  as c\n     on p._record_hash = c._parent_hash\nRESULT:\n{  "name": "Ana",  "age": "30",  "parent_id": "456",  "child_name": "Bill",  "child_id": "625",  "child_order_in_list": "0"}\n{  "name": "Ana",  "age": "30",  "parent_id": "456",  "child_name": "Elli",  "child_id": "591",  "child_order_in_list": "1"}\n{  "name": "Bob",  "age": "30",  "parent_id": "455",  "child_name": "Bill",  "child_id": "625",  "child_order_in_list": "0"}\n{  "name": "Bob",  "age": "30",  "parent_id": "455",  "child_name": "Dave",  "child_id": "621",  "child_order_in_list": "1"}\n\n```\n\n\n### 7. Run it yourself - plug your own iterator or generator.\nWorking example:\n[quickstart.py](examples/quickstart.py)',
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
