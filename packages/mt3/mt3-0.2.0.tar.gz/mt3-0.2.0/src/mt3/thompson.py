# -*- coding: utf-8 -*-
"""Modified Thompson Tau test for outlier detection

This module provide a function to perform Modified Thompson Tau test for outlier
detection

Reference for the Modified Thompson Tau test: 
    https://en.wikipedia.org/wiki/Outlier#Modified_Thompson_Tau_test
"""
import math

from typing import Iterable, List, Union
from .student import get_rejection_threshold

try:
    import numpy
except:
    numpy = None

try:
    import pandas
except ImportError:
    pandas = None

# Create an alias for possible sample type
if numpy is None and pandas is None:
    Sample = Iterable
    Outliers = List[bool]
elif pandas is None:
    Sample = Union[Iterable, numpy.ndarray]
    Outliers = Union[List[bool], numpy.ndarray]
elif numpy is None:
    Sample = Union[Iterable, pandas.Series]
    Outliers = Union[List[bool], numpy.ndarray]
else:
    Sample = Union[Iterable, numpy.ndarray, pandas.Series]
    Outliers = Union[List[bool], numpy.ndarray]


def mean(sample: Sample, where: List[bool] = None) -> float:
    """Return the mean of a sample

    Parameters
    ----------
    sample : {Iterable, pandas.Series}
       A sample

    where : {List[bool]}
        Elements to include in the mean

    Returns
    -------
    float
        The mean of the sample
    """
    if pandas is not None and isinstance(sample, pandas.Series):
        sample = sample.values

    if numpy is not None and isinstance(sample, numpy.ndarray):
        if where is not None:
            return sample.mean(where=where)
        else:
            return sample.mean()
    else:
        if where:
            sample = [s for include, s in zip(where, sample) if include]

        return sum(sample) / len(sample)


def std(sample: Sample, where=None, sample_mean=None, ddof: int = 1) -> float:
    """Return the standard deviation of a sample

    The parameter ddof is used to apply the Bessel's correction to
    correct the bias in the estimation of the sample variance

    Reference for Bessel's correction:
        https://en.wikipedia.org/wiki/Bessel%27s_correction

    Parameters
    ----------
    sample : {Iterable, pandas.Series}
       A sample

    where : {List[bool]}
        Elements to include in the mean

    sample_mean : {float}
       If known, mean of the sample can be provided so it will be reuse
       for standard deviation calculus

    ddof : {int}
       Delta Degrees of Freedom. The divisor used in calculations is
       N - ddof, where N represents the number of elements.

    Returns
    -------
    float
        The standard deviation of the sample
    """
    if pandas is not None and isinstance(sample, pandas.Series):
        sample = sample.values

    if numpy is not None and isinstance(sample, numpy.ndarray):
        if where is not None:
            return sample.std(where=where, ddof=ddof)
        else:
            return sample.std(ddof=ddof)
    else:
        if where:
            sample = [s for include, s in zip(where, sample) if include]

        m = mean(sample) if sample_mean is None else sample_mean

        return math.sqrt(sum([(s - m) ** 2 for s in sample]) / (len(sample) - ddof))


def modified_thompson_tau_test_step(
    sample: Sample, conf_level: float, where: list = None
) -> int:
    """One step of Modified Thompson Tau test for outlier detection

    Parameters
    ----------
    sample : {Iterable, pandas.Series}
        A sample on which perform the outlier detection

    conf_level: {float}
        Confidence level

    where : {List[bool], numpy.ndarray}
        Elements to include in the test

    Returns
    -------
    int
        Indice of the next outlier if there is one

    """
    if where is None:
        where = [True] * len(sample)

    m = mean(sample, where=where)
    s = std(sample, where=where, sample_mean=m)

    if s == 0:
        return False, None

    if pandas is not None and isinstance(sample, pandas.Series):
        sample = sample.values

    n = sum(where)
    threshold = get_rejection_threshold(n, conf_level)

    element_delta = 0
    element_ind = None

    for ind, (element, element_included) in enumerate(zip(sample, where)):
        if element_included:
            delta = abs((element - m) / s)

            if (delta > element_delta) and (delta > threshold):
                element_delta = delta
                element_ind = ind

    return element_ind


def modified_thompson_tau_test(
    sample: Sample, conf_level: float, nan_is_outlier: bool = False
) -> Outliers:
    """Perform a Modified Thompson Tau test for outlier detection

    Parameters
    ----------
    sample : {Iterable, pandas.Series}
        A sample on which perform the outlier detection

    conf_level: {float}
        Confidence level

    nan_is_outlier: {bool}
        True if nan should be considered as outliers

    Returns
    -------
    {List[bool], numpy.ndarray}
        List of boolean values indicating outliers

    """
    if pandas is not None and isinstance(sample, pandas.Series):
        sample = sample.values

    if numpy is not None and isinstance(sample, numpy.ndarray):
        remaining_points = ~numpy.isnan(sample)

    else:
        remaining_points = [True] * len(sample)

    while True:
        outlier = modified_thompson_tau_test_step(
            sample, conf_level, where=remaining_points
        )

        if outlier is None:
            break
        else:
            remaining_points[outlier] = False

    if numpy is not None and isinstance(remaining_points, numpy.ndarray):
        if nan_is_outlier:
            return ~remaining_points
        else:
            return ~remaining_points & ~numpy.isnan(sample)

    else:
        return [not remaining for remaining in remaining_points]
