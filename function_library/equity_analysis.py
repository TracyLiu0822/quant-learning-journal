"""Equity return and valuation utilities."""

import numpy as np
import pandas as pd


def daily_return(ticker, begdate, enddate):
    """
    Source: lecture02/lecture02.ipynb.

    Original function: ret_f.
    Downloads stock data and returns daily percentage returns.
    """
    import yfinance as yf

    df = yf.download(ticker, start=begdate, end=enddate)
    return df["Close"].pct_change().dropna()


def annual_return(ticker, begdate, enddate):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: ret_annual.
    Downloads stock data and computes annual returns from daily log returns.
    """
    import yfinance as yf

    df = yf.download(ticker, start=begdate, end=enddate)
    df["logret"] = np.log(df["Close"] / df["Close"].shift(1))
    df["year"] = df.index.year

    retannual = np.exp(df["logret"].groupby(df["year"]).sum()) - 1
    retannual = pd.DataFrame(retannual)
    retannual.columns = ["ret_" + ticker]

    return retannual


def compounded_group_return(returns):
    """
    Source: lecture02/lecture02.ipynb.

    Original lambda: lambda x: (1 + x).prod() - 1.
    Computes compounded return for a grouped return series.
    """
    return (1 + returns).prod() - 1


def gordon_growth_value(d1, r, g):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: gordon.
    Computes stock value with the Gordon growth model.
    """
    return d1 / (r - g)
