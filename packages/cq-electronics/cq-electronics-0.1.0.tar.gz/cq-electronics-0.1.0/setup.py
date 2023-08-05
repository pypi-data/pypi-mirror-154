# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cq_electronics',
 'cq_electronics.connectors',
 'cq_electronics.mechanical',
 'cq_electronics.rpi',
 'cq_electronics.smd']

package_data = \
{'': ['*']}

install_requires = \
['cadquery==2.2.0b0', 'casadi==3.5.5']

setup_kwargs = {
    'name': 'cq-electronics',
    'version': '0.1.0',
    'description': 'Pure CadQuery models of various electronic boards and components.',
    'long_description': '==============\ncq-electronics\n==============\n\n|build-status| |lint-status| |test-status| |docs-status|\n\nPure `CadQuery`_ models of various electronic boards and components.\n\nThese models are intended to be representations rather than detailed models.\nThat is, the major dimensions are accurate and there are enough features to make the component recognisable.\n\n\n.. _`CadQuery`: https://cadquery.readthedocs.io/\n\n.. |build-status| image:: https://github.com/sethfischer/cq-electronics/actions/workflows/build.yml/badge.svg\n    :target: https://github.com/sethfischer/cq-electronics/actions/workflows/build.yml\n    :alt: Build status\n.. |lint-status| image:: https://github.com/sethfischer/cq-electronics/actions/workflows/lint.yml/badge.svg\n    :target: https://github.com/sethfischer/cq-electronics/actions/workflows/lint.yml\n    :alt: Lint status\n.. |test-status| image:: https://github.com/sethfischer/cq-electronics/actions/workflows/test.yml/badge.svg\n    :target: https://github.com/sethfischer/cq-electronics/actions/workflows/test.yml\n    :alt: Test status\n.. |docs-status| image:: https://readthedocs.org/projects/cq-electronics/badge/?version=latest\n    :target: https://cq-electronics.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation status\n',
    'author': 'Seth Fischer',
    'author_email': 'seth@fischer.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sethfischer/cq-electronics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
