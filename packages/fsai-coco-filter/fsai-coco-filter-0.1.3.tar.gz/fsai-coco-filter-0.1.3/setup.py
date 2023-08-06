# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsai_coco_filter', 'fsai_coco_filter.tasks']

package_data = \
{'': ['*']}

install_requires = \
['echo1-coco-builder>=0.1.8,<0.2.0', 'loguru', 'pydash>=5.1.0,<6.0.0']

entry_points = \
{'console_scripts': ['coco-filter = fsai_coco_filter.fsai_coco_filter:app']}

setup_kwargs = {
    'name': 'fsai-coco-filter',
    'version': '0.1.3',
    'description': 'Apply filters to a coco annotation file from a project configuration file.',
    'long_description': '# fsai-coco-filter\n\nfsai-coco-filter provides a way to apply filters to a coco annotation file from a project configuration file.\n\n## Installation\n```shell\n# Install fsai-coco-filter\npip install fsai-coco-filter\n```\n\n## Add an fcf.json to your project\n```json\n{\n    "filter_annotations": [\n        "Powerline Pylon, Type A, H, Y",\n        "Powerline Pylon, Type I",\n        "Light Support Structure"\n    ],\n    "reset_category_ids": true,\n    "update_info": {\n        "year": 2022,\n        "version": "v1.0",\n        "contributor": "Foundation Stack AI",\n        "description": "Contact for more info.",\n        "url": "https://fsai.dev"\n    }\n}\n```\n\n# Run the coco-filter\nfsai-coco-filter \\\n    --input_file_path /tmp/coco.json \\\n    --output_file_path /tmp/coco-filtered.json\n\n\n## coco-filter help\n```shell\ncoco-filter\n\nusage: coco-filter [-h] -i INPUT_FILE_PATH -o OUTPUT_FILE_PATH [-c CONFIG_FILE]\ncoco-filter: error: the following arguments are required: -i/--input_file_path, -o/--output_file_path\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsai-dev/fsai-coco-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
