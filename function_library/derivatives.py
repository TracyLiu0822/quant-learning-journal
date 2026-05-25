"""Derivative payoff, Black-Scholes pricing, Greeks, and implied volatility."""

from math import exp, log, sqrt

import numpy as np
import scipy.stats as stats


def option_payoff(st, x, option_type="call"):
    """
    Source: lecture10/lecture10.ipynb.

    Merged from payoff_calls and payoff_put.
    Computes call or put payoff at maturity.
    """
    if option_type == "call":
        return (st - x + abs(st - x)) / 2
    if option_type == "put":
        return (abs(x - st) + x - st) / 2
    raise ValueError("option_type must be 'call' or 'put'")


def black_scholes_price(s, x, t, r, sigma, option_type="call"):
    """
    Source: lecture10/lecture10.ipynb, lecture11/lecture11.ipynb.

    Merged from bs_call, bs_put, bscall, bsCall.
    Computes Black-Scholes European call or put price.
    """
    d1 = (log(s / x) + (r + sigma * sigma / 2) * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)

    if option_type == "call":
        return s * stats.norm.cdf(d1) - x * exp(-r * t) * stats.norm.cdf(d2)
    if option_type == "put":
        return x * exp(-r * t) * stats.norm.cdf(-d2) - s * stats.norm.cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def implied_volatility(s, x, t, r, market_price, option_type="call", mode="best"):
    """
    Source: lecture10/lecture10.ipynb, lecture11/lecture11.ipynb.

    Merged from implied_vol_call, implied_vol_put, implied_vol_call_min,
    and implied_vol_put_min.

    mode='first' keeps the lecture10 threshold-search behavior and returns sigma.
    mode='best' keeps the lecture11 minimum-difference behavior and returns
    (k, implied_vol, model_price, min_abs_diff).
    """
    if mode == "first":
        for i in range(200):
            sigma = 0.005 * (i + 1)
            price = black_scholes_price(s, x, t, r, sigma, option_type)
            if abs(price - market_price) < 0.1:
                return sigma
        return None

    if mode != "best":
        raise ValueError("mode must be 'first' or 'best'")

    implied_vol = 1.0
    min_value = float("inf")
    best_price = None
    best_k = None

    for i in np.arange(1, 10000):
        sigma = 0.0001 * (i + 1)
        price = black_scholes_price(s, x, t, r, sigma, option_type)
        abs_diff = abs(price - market_price)

        if abs_diff <= min_value:
            min_value = abs_diff
            implied_vol = sigma
            best_price = price
            best_k = i

    return best_k, implied_vol, best_price, min_value


def implied_volatility_from_option_row(row, s, t, r, option_type="call", mode="best"):
    """
    Source: lecture11/lecture11.ipynb.

    Original lambda:
    lambda row: implied_vol_call_min(s, row['Strike'], t, r, row['Mid_Price']).
    Computes implied volatility from an option quote row with Strike and Mid_Price.
    """
    return implied_volatility(s, row["Strike"], t, r, row["Mid_Price"], option_type, mode)


def option_delta(s, x, t, r, sigma, method="closed_form", tiny=1e-11):
    """
    Source: lecture10/lecture10.ipynb, lecture11/lecture11.ipynb.

    Merged from delta_f, delta_n, delta1_f, delta2_f.
    Computes call option Delta by closed form or numerical difference.
    """
    if method == "closed_form":
        d1 = (log(s / x) + (r + sigma * sigma / 2) * t) / (sigma * sqrt(t))
        return stats.norm.cdf(d1)

    if method == "numerical":
        c1 = black_scholes_price(s, x, t, r, sigma, "call")
        c2 = black_scholes_price(s + tiny, x, t, r, sigma, "call")
        return (c2 - c1) / tiny

    raise ValueError("method must be 'closed_form' or 'numerical'")


def option_gamma(s, x, t, r, sigma, method="closed_form", tiny=1e-9, bump=1e-4):
    """
    Source: lecture11/lecture11.ipynb, lecture11/summary.md.

    Merged from gamma1_f, gamma2_f, gamma3_f.
    Computes call option Gamma by closed form, forward difference, or central difference.
    """
    if method == "closed_form":
        d1 = (log(s / x) + (r + sigma * sigma / 2) * t) / (sigma * sqrt(t))
        return stats.norm.pdf(d1) / (s * sigma * sqrt(t))

    if method == "forward":
        s1 = s
        s2 = s + bump
        s3 = s + 2 * bump
        c1 = black_scholes_price(s1, x, t, r, sigma, "call")
        c2 = black_scholes_price(s2, x, t, r, sigma, "call")
        c3 = black_scholes_price(s3, x, t, r, sigma, "call")
        return (c3 - 2 * c2 + c1) / (bump ** 2)

    if method == "central":
        s1 = s - tiny
        s2 = s
        s3 = s + tiny
        c1 = black_scholes_price(s1, x, t, r, sigma, "call")
        c2 = black_scholes_price(s2, x, t, r, sigma, "call")
        c3 = black_scholes_price(s3, x, t, r, sigma, "call")
        return (c3 - 2 * c2 + c1) / (tiny ** 2)

    raise ValueError("method must be 'closed_form', 'forward', or 'central'")
