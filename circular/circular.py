"""
Port of the circular functions needed to calculate the time periodic analyzer
Original circular project in gitlab/R7-Projects/circular

! _date2rad is different than circular.date2rad
"""
import numpy as np
from scipy.stats import vonmises
from scipy.optimize import minimize_scalar

import os
import os.path as op
import sys
sys.path.append(op.dirname(op.dirname(op.dirname(op.abspath(__file__)))))

def kernel(x, bw=10, n=256):
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

    #n_samples = x.shape[0]
    n_samples = len(x)

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
    
    # Standarized
    y_kernel = y_kernel / y_kernel.max()

    return y_kernel


def bwEstimation(x, lower= 0.1, upper= 500, xatol=1e-05):
    """Estimate the bandwidth/smoothing parameter for a the von Mises kernel
    based on the bw.cv.ml.circular function from  http://www.inside-r.org/packages/cran/circular/docs/bandwidth

    Parameters
    ----------
    x : array-like of shape = [n_samples] of radians.

    lower, upper: range over which to minimize for cross validatory bandwidths. The default is almost always
        satisfactory, although it is recommended experiment a little with different ranges.

    Returns
    -------
    bw : the bw that minimises the squared--error loss and Kullback--Leibler for the Von Mises pdf

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

    based on the bw.cv.ml.circular function from  http://www.inside-r.org/packages/cran/circular/docs/bandwidth

    Parameters
    ----------
    bw : the bandwidth for the Von Mises probability function

    x : array-like of shape = [n_samples] of radians.

    Returns
    -------
    result: cost of using bw in the log of the  Cross validatory Von Mises pdf

    """
    #n_samples = x.shape[0]
    n_samples = len(x)

    result = np.zeros(n_samples)
    for i in range(n_samples):
        result[i] = np.log(vonmises.pdf(np.delete(x,i,0), bw, loc=x[i]).sum(axis=0)/n_samples)
    result = result.sum(axis=0)/n_samples

    # 1 / result because Scipy dosent have maximize func
    result = 1 / result

    return result
