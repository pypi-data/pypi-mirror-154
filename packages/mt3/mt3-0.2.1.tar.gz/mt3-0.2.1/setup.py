# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mt3']

package_data = \
{'': ['*']}

extras_require = \
{'numpy': ['numpy>=1.22.4,<2.0.0'],
 'pandas': ['pandas>=1.4.2,<2.0.0'],
 'scipy': ['scipy>=1.8.1,<2.0.0']}

setup_kwargs = {
    'name': 'mt3',
    'version': '0.2.1',
    'description': 'A simple module for outlier detection thanks to Modified Thompson Tau Test',
    'long_description': '## Installation\n\n`mt3` requires Python 3.8+\n\nTo install the package run :\n\n```python\npip install mt3\n```\n\nIf you are planing to use it with [`numpy`](https://numpy.org/) and/or [`pandas`](https://pandas.pydata.org/docs/index.html), add optionnal dependencies :\n\n```python\npip install mt3[pandas, numpy] # or pip install mt3[numpy] for numpy only\n```\n\n`mt3` will then be capable to deal with `numpy.ndarray` and `pd.Series`.\n\nBy default `mt3` is provided with a table of [Student T critical values](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm). Available confidence levels are `[0.9, 0.95, 0.975, 0.99, 0.995, 0.999]`. To be able to use any confidence level, add `scipy` optionnal dependency :\n\n```python\npip install mt3[scipy]\n```\n\n## Usage\n\n`mt3` main function is `modified_thompson_tau_test` :\n\n```python\nfrom mt3 import modified_thompson_tau_test\n\nsample = [-4, 3, -5, -2, 0, 1, 1000]\n\n# You can use it with a simple list :\n\nmodified_thompson_tau_test(sample, 0.99)\n# [False, False, False, False, False, False, True]\n\n\n# But you can also use it with a numpy.ndarray or a pandas.Series\nimport numpy as np\nimport pandas as pd\n\nmodified_thompson_tau_test(np.array(sample), 0.99)\n# [False False False False False False True] (numpy array)\n\nmodified_thompson_tau_test(pd.Series(sample), 0.99)\n# [False False False False False False True] (numpy array)\n\n# If you have nan values in your array or Series, you can choose to treat\n# them as outliers\nsample_with_nan = np.array([-4, np.nan, 3, -5, -2, 0, 1, 1000])\n\nmodified_thompson_tau_test(sample_with_nan, 0.99, nan_is_outlier=True)\n# [False True False False False False False True] (numpy array)\n```\n',
    'author': 'h4c5',
    'author_email': 'hakimcheikh@yahoo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/h4c5/mt3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
