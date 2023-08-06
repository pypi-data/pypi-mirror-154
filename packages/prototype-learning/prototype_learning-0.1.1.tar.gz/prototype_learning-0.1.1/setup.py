# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prototype_learning']

package_data = \
{'': ['*']}

install_requires = \
['conda-lock>=1.0.5,<2.0.0',
 'numpy==1.20.3',
 'scikit-learn>=1.1.1,<2.0.0',
 'skorch>=0.11.0,<0.12.0',
 'torch==1.11.0']

setup_kwargs = {
    'name': 'prototype-learning',
    'version': '0.1.1',
    'description': 'A package for learning interpretable prototypes for prediction tasks.',
    'long_description': '# prototype_learning\n\nA package for learning interpretable prototypes for prediction tasks.\n\n## Installation\n\n```bash\n$ pip install prototype_learning\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`prototype_learning` was created by Anton Matsson. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`prototype_learning` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Anton Matsson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
