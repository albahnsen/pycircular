
import numpy as np
import pandas as pd
from scipy.stats import vonmises
from statsmodels.distributions.empirical_distribution import ECDF

import os
import os.path as op
import sys
sys.path.append(op.dirname(op.dirname(op.dirname(op.abspath(__file__)))))


def kuiper_two(x, y, return_all=False):
    """Compute the Kuiper statistic to compare two samples.
    # By Anne M. Archibald, 2007 and 2009, from
    https://github.com/aarchiba/kuiper/blob/master/kuiper.py

    Parameters
    ----------
    x : array-like
        The first set of data values.
    y : array-like
        The second set of data values.

    return_all: bool, whether to return additional info for plotting

    Returns
    -------
    fpp : float
        The probability of obtaining two samples this different from
        the same distribution.

    others : tuple, if return_all
        (z, d_cdf, k_cdf, D1_, D2_, D1, D2)

    Notes
    -----
    Warning: the fpp is quite approximate, especially for small samples.

    """
    n = y.shape[0]
    z = np.linspace(0, np.pi * 2, n)

    # X CDF
    d_cdf = ECDF(x)
    d_cdf = d_cdf(z)

    # Kernel CDF
    k_cdf = y.cumsum()
    k_cdf /= k_cdf.max()

    # Estimate D
    D1_, D2_ = np.argmax(d_cdf - k_cdf), np.argmax(k_cdf - d_cdf)
    D1 = (d_cdf - k_cdf)[D1_]
    D2 = (k_cdf - d_cdf)[D2_]
    D = D1 + D2

    Ne = len(x) * len(y) / float(len(x) + len(y))

    if return_all:
        return _kuiper_prob(D, Ne), (z, d_cdf, k_cdf, D1_, D2_, D1, D2)
    else:
        return _kuiper_prob(D, Ne)


def _kuiper_prob(D, N):
    """Compute the false positive probability for the Kuiper statistic.
    https://github.com/scottransom/presto/blob/master/lib/python/kuiper.py
    From section 14.3 in Numerical Recipes

    Parameters
    ----------
    D : float
        The Kuiper test score.
    N : float
        The effective sample size.

    Returns
    -------
    fpp : float
        The probability of a score this large arising from the null hypothesis.

    Reference
    ---------
    Press et al. "Numerical Recipes: The Art of Scientific Computing",
    3rd Edition, p.627, 2007.
    http://www2.units.it/ipl/students_area/imm2/files/Numerical_Recipes.pdf

    """
    
    # From section 14.3 in Numerical Recipes
    EPS1 = 1e-6
    EPS2 = 1e-12
    en = np.sqrt(N)
    lamda = (en + 0.155 + 0.24 / en) * D
    if (lamda < 0.4): return 1.0
    probks = termbf = 0.0
    a2 = -2.0 * lamda * lamda
    for ii in range(1, 100):
        a2ii2 = a2 * ii * ii
        term = 2.0 * (-2.0 * a2ii2 - 1.0) * np.exp(a2ii2)
        probks += term
        if (np.fabs(term) <= EPS1*termbf or
            np.fabs(term) <= EPS2*probks):
            return probks
        termbf = np.fabs(term)
    return 1.0

def periodic_mean_std(angles):
    """Calculate the periodic mean and std

    Parameters
    ----------
    angles : array-like or pandas.DataFrame of angles.
        Do not matter if it is radians or degrees

    Returns
    -------
    mean : float
        calculated periodic mean

    std : float
        calculated periodic std


    Examples
    --------
    >>> import numpy as np
    >>> from pycircular.stats import periodic_mean_std
    >>> angles = np.array([0, 1, 2, 4, 6, 7, 8])
    >>> print(angles.mean(), angles.std())
    >>> print(periodic_mean_std(angles))

    """

    sin_ = np.sin(angles)
    cos_ = np.cos(angles)
    n_ = len(angles)

    if isinstance(angles, pd.DataFrame):
        mean = np.arctan2(sin_.mean(), cos_.mean()).values[0]
        R = np.sqrt(sin_.sum()**2 + cos_.sum()**2) / n_
        std = np.sqrt(-2 * np.log(R)).values[0]

    else:
        mean = np.arctan2(np.mean(sin_), np.mean(cos_))
        R = np.sqrt(np.sum(sin_)**2 + np.sum(cos_)**2) / n_
        std = np.sqrt(-2 * np.log(R))

    return mean, std


def von_mises_distribution(mean, std, size=240):
    """Calculate the von Mises distribution

    Parameters
    ----------
    mean : float
        calculated periodic mean

    std : float
        calculated periodic std

    Returns
    -------
    x : array-like of shape [size]
        radians across the circle

    p : array-like of shape [size]
        von Mises pdf for each value of x

    """
    x = np.linspace(-np.pi, np.pi, size)
    p = vonmises.pdf(x, 1/std)
    x += mean

    return x, p