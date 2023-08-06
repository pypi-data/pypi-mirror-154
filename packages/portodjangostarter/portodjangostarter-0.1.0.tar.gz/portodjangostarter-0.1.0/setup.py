# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portodjangostarter',
 'portodjangostarter._app_template.migrations',
 'portodjangostarter._app_template.models',
 'portodjangostarter._app_template.tests',
 'portodjangostarter.management',
 'portodjangostarter.management.commands']

package_data = \
{'': ['*'],
 'portodjangostarter': ['_app_template/*',
                        '_app_template/actions/*',
                        '_app_template/tasks/*',
                        '_app_template/ui/api/controllers/*',
                        '_app_template/ui/api/routes/*',
                        '_app_template/ui/api/transformers/*']}

install_requires = \
['Django>=3.2,<4.0', 'djangorestframework>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'portodjangostarter',
    'version': '0.1.0',
    'description': 'With portodjangostarter we can start porto containers in django project',
    'long_description': None,
    'author': 'BakdauletBolat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
