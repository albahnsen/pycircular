"""
Base IO code for all datasets
https://github.com/scikit-learn/scikit-learn/blob/56057c9630dd13f3c61fbb4c7debdff6ba8e9e8c/sklearn/datasets/base.py
"""

# Copyright (c) 2007 David Cournapeau <cournape@gmail.com>
#               2010 Fabian Pedregosa <fabian.pedregosa@inria.fr>
#               2010 Olivier Grisel <olivier.grisel@ensta.org>
#               2014, 2023 Alejandro CORREA BAHNSEN <al.bahnsen@gmail.com>
# License: BSD 3 clause

from os.path import dirname
from os.path import join
import numpy as np
import pandas as pd


class Bunch(dict):
    """Container object for datasets: dictionary-like object that
       exposes its keys as attributes."""
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


def load_transactions():
    """Load and return the transactions' dataset (classification).

    The bank transactions is an easily transformable transactional dataset.

    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the classification labels,
        meaning of the features, and 'DESCR', the full description of the dataset.

    References
    ----------
    .. [1] A. Correa Bahnsen, A. Stojanovic, D.Aouada, B, Ottersten,
           `"Improving Credit Card Fraud Detection with Calibrated Probabilities" <http://albahnsen.com/files/%20Improving%20Credit%20Card%20Fraud%20Detection%20by%20using%20Calibrated%20Probabilities%20-%20Publish.pdf>`__, in Proceedings of the fourteenth SIAM International Conference on Data Mining,
           677-685, 2014.

    Examples
    --------
    >>> from circular.datasets import load_transactions
    >>> data = load_transactions()
    >>> data.data.head()
    """
    module_path = dirname(__file__)
    raw_data = pd.read_csv(join(module_path, 'data', 'transactions.csv.gz'),
                           delimiter=',', compression='gzip', index_col=0)
    # TODO: descr = open(join(module_path, 'descr', 'transactions.rst')).read()
    descr = ''

    return Bunch(data=raw_data, DESCR=descr,
                 feature_names=raw_data.columns.values, name='Transactions')
