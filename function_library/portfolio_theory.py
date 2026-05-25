"""Portfolio risk, return, and Sharpe ratio utilities."""

import numpy as np


def lower_partial_standard_deviation(returns, rm):
    """
    Source: lecture07/lecture7.ipynb.

    Original function: lpsd_f.
    Computes lower partial standard deviation relative to a benchmark return.
    """
    y = returns[returns < rm]
    total = 0.0
    m = len(y)

    for r in y:
        total += (r - rm) ** 2

    var = total / (m - 1)
    return round(np.sqrt(var), 5)


def two_stock_variance(wa, vara, varb, covab):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: var2stock.
    Computes two-stock portfolio variance.
    """
    wb = 1 - wa
    return wa ** 2 * vara + wb ** 2 * varb + 2 * wa * wb * covab


def portfolio_variance(r, w):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: portfolio_var.
    Computes multi-asset portfolio variance using correlation and standard deviation.
    """
    r = np.asarray(r)
    w = np.asarray(w)
    n = len(w)
    cor = np.corrcoef(r.T)
    std_dev = np.std(r, axis=0)
    var = 0

    for i in range(n):
        for j in range(n):
            var += w[i] * w[j] * std_dev[i] * std_dev[j] * cor[i, j]

    return var


def sharpe_ratio(r, w, rf):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: sharperatio.
    Computes portfolio Sharpe ratio.
    """
    var = portfolio_variance(r, w)
    mean_return = np.mean(r, axis=0)
    port_return = np.dot(w, mean_return)
    return (port_return - rf) / np.sqrt(var)


def negative_sharpe_ratio_from_n_minus_1_weights(w, r, rf):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: sharperatio_n_minus_1_stocks.
    Builds the final portfolio weight as 1 - sum(w) and returns negative Sharpe ratio.
    """
    w2 = np.append(w, 1 - sum(w))
    return -sharpe_ratio(r, w2, rf)
