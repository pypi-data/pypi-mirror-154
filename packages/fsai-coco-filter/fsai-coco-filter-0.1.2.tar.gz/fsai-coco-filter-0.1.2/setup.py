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
    'version': '0.1.2',
    'description': 'Apply filters to a coco annotation file from a project configuration file.',
    'long_description': '# fsai-coco-filter',
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
