"""
Port of the circular functions needed to calculate the time periodic analyzer
Original circular project in gitlab/R7-Projects/circular

! _date2rad is different than circular.date2rad

"""

import pandas as pd
import numpy as np
from scipy.stats import vonmises
from scipy.optimize import minimize_scalar
#from scipy.misc import factorial, comb
from statsmodels.distributions.empirical_distribution import ECDF
import itertools


def _kuiper_two(x, y, return_all=False):
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


def _kernel(x, bw=10, n=256):
    """Estimate the von Mises kernel

    Parameters
    ----------
    x : array-like of shape = [n_samples] of radians.

    bw : Bandwidth of the kernel estimation
        The bandwidth is related to the width of the individual von Mises distributions

    n : number of points of the kernel

    Returns
    -------
    y : array-like of shape = [n]
        Calculated von Mises kernel

    """

    n_samples = x.shape[0]

    # The points of the circumference
    z = np.linspace(0, np.pi * 2, n)

    # Estimate one von Mises for each point centered in x[i] with kappa = bw
    y = np.zeros((n_samples, n))

    # As all von Mises are equal so only estimate one
    p = vonmises.pdf(z, bw)

    # TODO: calculate in numba or Cython
    for i in range(n_samples):
        # Reposition the estimated von Mises
        # Idx aprox the point x[i] to a point in z
        idx = np.abs(z - x[i]).argmin()
        if idx == 0:
            y[i, :] = p
        else:
            y[i, idx:] = p[:-idx]
            y[i, :idx] = p[-idx:]
            # Position idx is equal to p[0]
            # Position idx-1 is equal to p[-1]

    # Sum all the vonmises
    y_kernel = y.sum(axis=0) / n_samples

    return y_kernel


def _bwEstimation(x, lower= 0.1, upper= 500, xatol=1e-05):
    """Estimate the bandwidth/smoothing parameter for a the von Mises kernel
    based on the bw.cv.ml.circular function from  http://www.inside-r.org/packages/cran/circular/docs/bandwidth
​
    Parameters
    ----------
    x : array-like of shape = [n_samples] of radians.
​
    lower, upper: range over which to minimize for cross validatory bandwidths. The default is almost always
        satisfactory, although it is recommended experiment a little with different ranges.
​
    Returns
    -------
    bw : the bw that minimises the quared--error loss and Kullback--Leibler for the Von Mises pdf

    """
    if(len(x)<2):
        raise Exception("Need at least 2 data points")
    bw = minimize_scalar(_costFunction, args=x, bounds=(lower, upper), method="Bounded", 
                         options={'maxiter': 500, 'xatol': xatol})
    return bw.x


def _costFunction(bw, x):
    """
    Cross validatory bandwidths minimizing squared--error loss and Kullback--Leibler loss, respectively
    This is done by minimizing the second and third equations in section 5 of Hall, Watson and Cabrera (1987).
    Kullback--Leibler loss is equivalent to maximize the cross validation log--likelihood with respect to the bandwidth parameter.
​
    based on the bw.cv.ml.circular function from  http://www.inside-r.org/packages/cran/circular/docs/bandwidth
​
    Parameters
    ----------
    bw : the bandwidth for the Von Mises probability function
​
    x : array-like of shape = [n_samples] of radians.
​
    Returns
    -------
    result: cost of using bw in the log of the  Cross validatory Von Mises pdf
​
    """
    n_samples = x.shape[0]

    result = np.zeros(n_samples)
    for i in range(n_samples):
        result[i] = np.log(vonmises.pdf(np.delete(x,i,0), bw, loc=x[i]).sum(axis=0)/n_samples)
    result = result.sum(axis=0)/n_samples

    # 1 / result because Scipy dosent have maximize func
    result = 1 / result

    return result


def _date2rad(dates, time_segment='hour'):
    """Convert time_segment to radians

    From circular.utils.date2rad and circular.utils.freq_time

    Parameters
    ----------
    dates : pandas DatetimeIndex array-like of shape = [n_samples] of dates.

    time_segment: string of values ['hour', 'dayweek', 'daymonth']

    Returns
    -------
    radians : array-like of shape = [n_samples]
        Calculated radians

    """

    # calculate times
    times = dates.hour + dates.minute / 60 + dates.second / 60 / 60  
    # Change from 100 to 60, consistency for radians

    if time_segment == 'hour':

        radians = times * 2 * np.pi / 24

        # Fix to rotate the clock and move PI / 2
        # https://en.wikipedia.org/wiki/Clock_angle_problem

        radians = - radians + np.pi/2

    elif time_segment == 'dayweek':

        time_temp = dates.dayofweek  # Monday=0, Sunday=6
        times = time_temp + times / 24

        # Day of week goes counter-clockwise
        radians = times * 2 * np.pi / 7 + np.pi/2

    elif time_segment == 'daymonth':

        time_temp = dates.day
        times = time_temp + times / 24

        # Day of month goes counter-clockwise
        radians = times * 2 * np.pi / 31 + np.pi/2
        # TODO: check what to do with last day of month

    # Change to be in range [0, 2*pi]
    if hasattr(radians, 'shape'):
        # Check if an array
        radians[radians < 0] += 2 * np.pi
        radians[radians > 2 * np.pi] -= 2 * np.pi
    else:
        # If it is a scalar
        if radians < 0:
            radians += 2 * np.pi
        elif radians > 2 * np.pi:
            radians -= 2 * np.pi

    return radians