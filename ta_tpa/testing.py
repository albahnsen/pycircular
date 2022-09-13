
import pandas as pd
import numpy as np

from .circular import _date2rad

def test_time_periodic(trx_test, risk_all, min_confidence=0.85, combination_weights=[0.5, 0.2, 0.3]):
    """Evaluate the time periodic risk of a transaction

    Parameters
    ----------
    trx_test : pd.DataFrame of the transactions

    risks_all : dictionary of shape n_accounts where each value is a
        pd.DataFrame of shape = [3, n + 1] for each account
        where the rows are the different time segments ['hour', 'dayweek', 'daymonth']
        the columns are the n points of the kernel and the confidence of the kernel

    min_confidence = minimum confidence of the kernels, default=0.85

    combination_weights = list of the weights for each kernel default = [0.5, 0.2, 0.3]

    Returns
    -------
    risks : pandas DataFrame of shape [n_samples, 3]
        where the columns are the transaction ID, date  and the estimated risk

    """


    n_samples = trx_test.shape[0]

    # Initialite the resulting DataFrame
    risks = pd.DataFrame(index=trx_test.index)
    risks['transactionId'] = trx_test['transactionId'].copy()
    risks['date'] = trx_test['date'].copy()
    risks['PeriodicTimeRisk'] = np.nan

    # Convert dates
    dates = pd.DatetimeIndex(trx_test['date'])

    # For each transaction
    for i in range(n_samples):
        date = dates[i]
        account = trx_test['account'].iloc[i]
        risks.loc[i, 'PeriodicTimeRisk'] = _test_time_periodic_trx(date, account, risk_all=risk_all,
                                                                   min_confidence=min_confidence,
                                                                   combination_weights=combination_weights)

    return risks


def _test_time_periodic_trx(date, account, risk_all, min_confidence=0.85, combination_weights=[0.5, 0.2, 0.3]):
    """Evaluate the time periodic risk of a transaction

    Parameters
    ----------
    date : pandas DatetimeIndex array-like of shape = [1].

    account : int like with the account number

    risks_all : dictionary of shape n_accounts where each value is a
        pd.DataFrame of shape = [3, n + 1] for each account
        where the rows are the different time segments ['hour', 'dayweek', 'daymonth']
        the columns are the n points of the kernel and the confidence of the kernel

    min_confidence = minimum confidence of the kernels, default=0.85

    combination_weights = list of the weights for each kernel default = [0.5, 0.2, 0.3]

    Returns
    -------
    risk : int of the estimated risk, np.nan if cant be evaluated

    """

    # Estimate the number of points and create the default linspace
    n = list(risk_all.values())[0].shape[1] - 1
    z = np.linspace(0, 2 * np.pi, n)

    if account in risk_all.keys():

        risks = risk_all[account]
        risks_ = np.empty(3)

        for i, time_segment in enumerate(['hour', 'dayweek', 'daymonth']):

            # Check the confidence of kernel
            if risks.loc[time_segment, 'Risk_confidence'] < min_confidence:
                risks_[i] = np.nan

            else:

                # Convert current times to radials
                radian = _date2rad(date, time_segment=time_segment)

                # Find location of the current times in the kernel
                loc_ = np.argmin(np.abs(z - radian))

                # Find the risk and the pvalue
                risks_[i] = risks.loc[time_segment, 'Risk_p' + str(loc_)]

        # Combination
        # 0.5 0.2, 0.3 # From previous model

        # if all different from NaN
        temp = np.array(combination_weights)[~np.isnan(risks_)].sum()

        # Check if at least one risk is different than np.nan
        if temp == 0:
            return np.nan
        else:
            # Combine the different risks
            risk = np.multiply(risks_, combination_weights)
            risk = risk[~np.isnan(risks_)].sum()
            risk /= temp
            return round(risk)
    else:
        return np.nan
