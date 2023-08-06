## Installation

`mt3` requires Python 3.8+

To install the package run :

```python
pip install mt3
```

If you are planing to use it with [`numpy`](https://numpy.org/) and/or [`pandas`](https://pandas.pydata.org/docs/index.html), add optionnal dependencies :

```python
pip install mt3[pandas, numpy] # or pip install mt3[numpy] for numpy only
```

`mt3` will then be capable to deal with `numpy.ndarray` and `pd.Series`.

By default `mt3` is provided with a table of [Student T critical values](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm). Available confidence levels are `[0.9, 0.95, 0.975, 0.99, 0.995, 0.999]`. To be able to use any confidence level, add `scipy` optionnal dependency :

```python
pip install mt3[scipy]
```

## Usage

`mt3` main function is `modified_thompson_tau_test` :

```python
from mt3 import modified_thompson_tau_test

sample = [-4, 3, -5, -2, 0, 1, 1000]

# You can use it with a simple list :

modified_thompson_tau_test(sample, 0.99)
# [False, False, False, False, False, False, True]


# But you can also use it with a numpy.ndarray or a pandas.Series
import numpy as np
import pandas as pd

modified_thompson_tau_test(np.array(sample), 0.99)
# [False False False False False False True] (numpy array)

modified_thompson_tau_test(pd.Series(sample), 0.99)
# [False False False False False False True] (numpy array)

# If you have nan values in your array or Series, you can choose to treat
# them as outliers
sample_with_nan = np.array([-4, np.nan, 3, -5, -2, 0, 1, 1000])

modified_thompson_tau_test(sample_with_nan, 0.99, nan_is_outlier=True)
# [False True False False False False False True] (numpy array)
```
