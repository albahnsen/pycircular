
import pandas as pd
import numpy as np

from .circular import bwEstimation, kernel
from .utils import _date2rad
from .stats import kuiper_two


def train_time_periodic(trx_train, n=256, idname='account'):
    """Evaluate the time periodic risk of different accounts

    Parameters
    ----------
    trx_train : pd.DataFrame of the transactions

    n : number of points of the kernel

    Returns
    -------
    risks_all : dictionary of shape n_accounts where each value is a
        pd.DataFrame of shape = [3, n + 1] for each account
        where the rows are the different time segments ['hour', 'dayweek', 'daymonth']
        the columns are the n points of the kernel and the confidence of the kernel

    """

    # For each account
    accounts = trx_train[f'{idname}'].unique()

    risks_all = dict()
    for account in accounts:
        dates = trx_train.query(f'{idname} == {account}')['date']
        risks_all[account] = _train_time_periodic_account(dates, n=256)

    return risks_all


def _train_time_periodic_account(dates, n=256,
                                 time_segments=('hour', 'dayweek', 'daymonth')):
    """Evaluate the time periodic risk of a set of dates

    Parameters
    ----------
    dates : pandas DatetimeIndex array-like of shape = [n_samples] of dates.

    n : number of points of the kernel

    #TODO timesegments

    Returns
    -------
    risks : pd.DataFrame of shape = [3, n + 1]
        where the rows are the different time segments ['hour', 'dayweek', 'daymonth']
        the columns are the n points of the kernel and the confidence of the kernel

    """

    # Create the DataFrame to store the results
    risks = pd.DataFrame(np.nan, index=time_segments,
                         columns=['Risk_p' + str(i) for i in range(n)] +
                                 ['Risk_confidence', 'bw'])

    for time_segment in time_segments:

        radians = _date2rad(dates, time_segment=time_segment).to_list()

        # Find bw
        bw = bwEstimation(radians, upper=500)

        # Estimate kernel
        y = kernel(radians, bw=bw, n=n)

        # Test the kernel
        p = kuiper_two(radians, y)

        risks.loc[time_segment].iloc[:-2] = np.round((1 - (y / y.max())) * 100)
        risks.loc[time_segment].iloc[-2] = p
        risks.loc[time_segment].iloc[-1] = bw

    return risks