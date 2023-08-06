# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ontorunner',
 'ontorunner.converters',
 'ontorunner.pipes',
 'ontorunner.post',
 'ontorunner.pre']

package_data = \
{'': ['*']}

install_requires = \
['OGER>=1.5,<2.0',
 'click>=8.1.3,<9.0.0',
 'dframcy>=0.1.6,<0.2.0',
 'kgx>=1.5.8,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scispacy==0.5.0',
 'six>=1.16.0,<2.0.0',
 'spacy>=3.2.0,<3.3.0',
 'textdistance[extras]>=4.2.2,<5.0.0']

setup_kwargs = {
    'name': 'ontorunner',
    'version': '0.1.0.dev0',
    'description': 'This repository is a wrapper project around various entity recognition (NER) tools.',
    'long_description': None,
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
