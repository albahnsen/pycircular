
import pandas as pd
import numpy as np

from .circular import bwEstimation, _date2rad, kernel, _kuiper_two


def train_time_periodic(trx_train, n=256):
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
    accounts = trx_train['account'].unique()

    risks_all = dict()
    for account in accounts:
        dates = pd.DatetimeIndex(trx_train.query('account == ' + str(account))['date'])
        risks_all[account] = _train_time_periodic_account(dates, n=256)

    return risks_all


def _train_time_periodic_account(dates, n=256):
    """Evaluate the time periodic risk of a set of dates

    Parameters
    ----------
    dates : pandas DatetimeIndex array-like of shape = [n_samples] of dates.

    n : number of points of the kernel

    Returns
    -------
    risks : pd.DataFrame of shape = [3, n + 1]
        where the rows are the different time segments ['hour', 'dayweek', 'daymonth']
        the columns are the n points of the kernel and the confidence of the kernel

    """

    time_segments = ['hour', 'dayweek', 'daymonth']

    # Create the DataFrame to store the results
    risks = pd.DataFrame(np.nan, index=time_segments,
                         columns=['Risk_p' + str(i) for i in range(n)] +
                                 ['Risk_confidence'])

    for time_segment in time_segments:

        radians = _date2rad(dates, time_segment=time_segment)

        # Find bw
        bw = bwEstimation(radians, upper=500)

        # Estimate kernel
        y = kernel(radians, bw=bw, n=n)

        # Test the kernel
        p = _kuiper_two(radians, y)

        risks.loc[time_segment].iloc[:-1] = np.round((1 - (y / y.max())) * 100)
        risks.loc[time_segment].iloc[-1] = p

    return risks