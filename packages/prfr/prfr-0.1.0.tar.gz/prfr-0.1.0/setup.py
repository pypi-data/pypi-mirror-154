# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prfr']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy<1.22',
 'scipy>=1.8.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'prfr',
    'version': '0.1.0',
    'description': '',
    'long_description': '# prfr\n\nProbabilistic random forest regressor\n',
    'author': 'Jeff Shen',
    'author_email': 'jshen2014@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
