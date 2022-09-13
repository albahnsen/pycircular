
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import operator
from matplotlib.ticker import FuncFormatter
import seaborn as sns
current_palette = sns.color_palette()
import matplotlib.ticker as mticker

import os
import os.path as op
import sys
sys.path.append(op.dirname(op.dirname(op.dirname(op.abspath("__file__")))))

from circular.utils import date2rad
from circular.stats import periodic_mean_std, von_mises_distribution
from circular.stats import kuiper_two


def base_periodic_fig(dates, freq, bottom=0, ymax=1,
                      rescale=True, figsize=(8, 8),
                      time_segment='hour', fig=None, ax1=None):
    """Base figure for plotting periodic time variables

    Parameters
    ----------
    dates : array-like of shape = [unique_n_samples] of dates in format 'datetime64[ns]'.

    freq : array-like of shape = [unique_n_samples] of frequencies for each date.

    # TODO: finish

    time_segment: string of values ['hour', 'dayweek', 'daymonth']

    Returns
    -------
    fig, ax : Figure and axis objects

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> import matplotlib.pyplot as plt
    >>> from circular.utils import freq_time, date2rad
    >>> from circular.plots import base_periodic_fig
    >>> dates = pd.to_datetime(["2013-10-02 19:10:00", "2013-10-21 19:00:00", "2013-10-24 3:00:00"])
    >>> time_segment = 'dayweek'  # 'hour', 'dayweek', 'daymonth
    >>> freq_arr, times = freq_time(dates, time_segment=time_segment)
    >>> fig, ax1 = base_periodic_fig(freq_arr[:, 0], freq_arr[:, 1], time_segment=time_segment)
    """

    if rescale:
        freq = freq / freq.max()
        ymax = 1.

    angles = date2rad(dates, time_segment)

    if fig is None:
        fig = plt.figure(figsize=figsize)
        ax1 = plt.subplot(111, polar=True)

    # Define figure parameters
    width = (2*np.pi)

    if time_segment == 'hour':
        width /= 30
        ticks_loc = ax1.get_xticks().tolist()
        ax1.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
        ax1.set_xticklabels(['6h', '3h', '0h', '21h', '18h', '15h', '12h', '9h'])
        angles=[i+(width/2) for i in angles]

    elif time_segment == 'dayweek':
        width /= 30
        temp_xticks = np.linspace(np.pi/2, 2*np.pi+np.pi/2, 7, endpoint=False)
        temp_xticks[-1] -= 2 * np.pi
        ax1.set_xticks(temp_xticks)
        ticks_loc = ax1.get_xticks().tolist()
        ax1.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
        ax1.set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        angles=[i-(width) for i in angles]
        # TO DO: check the shift amount for good visualization
        # angles=[i-(width/2) for i in angles] ?

    elif time_segment == 'daymonth':
        width /= 31
        temp_xticks = np.linspace(np.pi/2, 2*np.pi+np.pi/2, 31, endpoint=False)
        temp_xticks[temp_xticks>2*np.pi] -= 2 * np.pi
        ax1.set_xticks(temp_xticks)
        ticks_loc = ax1.get_xticks().tolist()
        ax1.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
        ax1.set_xticklabels(range(1, 32))
        angles=[i-(width/2) for i in angles]
        # TODO: what to do with 31

    ax1.bar(angles, freq, width=width, bottom=bottom, alpha=0.5)
    ax1.set_ylim([0, bottom+ymax])

    ax1.set_yticklabels([])
    return fig, ax1

# TODO: Inherit the properties from base_clock. Probably as a class
def clock_vonmises_distribution(ax1, mean, x, p, rescale=True):
    # TODO: add description

    if rescale:
        p = p / p.max()

    # Plot the mean
    ax1.plot([mean, mean], [0, 1], c=current_palette[1], ls='--', linewidth=5)

    # Plot the distribution
    ax1.plot(x, p, c=current_palette[1], ls='-', linewidth=2)
    ax1.fill_between(x, 0, p, alpha=0.5, color=current_palette[1])

    return ax1


def plot_CDF_kernel(x, y):
    """Plot of the CDF kernel and kuiper test

    Parameters
    ----------
    x : array-like of shape = [n_samples] of radians.

    y : array-like of the kernel density.

    Returns
    -------
    fig, ax : Figure and axis objects

    Examples
    --------
    >>> import numpy as np
    >>> from circular.density import kernel, bwEstimation
    >>> from circular.density_tests import kuiper_two
    >>> from circular.plots import plot_CDF_kernel
    >>> x = np.array([0.8 ,  1.  ,  1.1 ,  1.15,  4.  ,  4.2 ,  4.3 ,  4.4])
    >>> bw = bwEstimation(x, upper=500)
    >>> y = kernel(x, bw=2)
    >>> fig, ax1 = plot_CDF_kernel(x, y)
    """

    p, (z, d_cdf, k_cdf, D1_, D2_, D1, D2) = kuiper_two(x, y, return_all=True)

    fig = plt.figure()
    ax1 = plt.subplot(111)
    ax1.plot(z, d_cdf)
    ax1.plot(z, k_cdf)
    ax1.plot([z[D1_], z[D1_]], [d_cdf[D1_], k_cdf[D1_]], c='r', lw=5)
    ax1.plot([z[D2_], z[D2_]], [d_cdf[D2_], k_cdf[D2_]], c='r', lw=5)

    return fig, ax1



