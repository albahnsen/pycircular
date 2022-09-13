# Time Periodic Analyzer

### Authors:
- Alejandro Correa Bahnsen 
- Sergio Villegaas
- Juan Sebastián Salcedo Gallo
- Jesús Solano
- Victor Maya
- Cesar Charalla
- Hernán García

__version__ = '1.0'

__date__ = 13/09/2022


## Motivation
When constructing a fraud detection model, it is very important to use those features that allow accurate classification. Typical models only use raw transactional features, such as time, amount and place of the transaction. However, these approaches do not take into account the spending behavior of the customer, which is expected to help discover fraud patterns. A standard way to include these behavioral spending patterns consists of using aggregated features that creates a customer behavioral profile by grouping the transactions that each customer made during the last given number of hours, first by card or account number, then by transaction type, merchant group, country or other, followed by calculating the number of transactions and the total amount spent on those transactions.

However, when using the aggregated features, there is still some information that is not captured correctly by those features. For example, in only using aggregated features, it is not possible to have an accurate time frame of when a customer is expected to make new transactions. Moreover, the issue when dealing with the time of the transaction, and specifically, when analyzing a feature such as the mean of transactions time, it is easy to make the mistake of using the arithmetic mean. Indeed, the arithmetic mean is not a correct way to average time because it does not take into account the periodic behavior of the time feature.
## New analyzer
The new analyzer is based is modeling the periodic behavior of the time of a transaction, i.e., hour of the day
day of the week or day of the month. By adjusting a non-linear non-parametric kernel distribution, the new
analyzer is able to estimate the expected time of transaction and evaluate wether a new transactions is being made at normal hours / days.
## Examples

### Technical description of the analyzer
See /Tests/TA_TPA_technical_presentation.ipynb

### Practial example
See /tests/example_tpa.ipynb

By-step examples:
- See /tests/example_tpa_bystep_training.ipynb
- See /tests/example_tpa_bystep_testing.ipynb

To open use ipython notebook and navigate to the file

## Requirements
Build using
`Python 3.5.0 |Anaconda 2.4.0 (64-bit)| (default, Oct 19 2015, 21:57:25)`. For the technical example
it is needed to install the `circular` package available at gitlab and `conda install seaborn`.

All the dependencies are included in Anaconda 2.4.0
