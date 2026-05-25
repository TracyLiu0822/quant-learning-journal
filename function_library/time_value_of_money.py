"""Time value of money utilities."""

from math import exp, log


def annuity_value(c, r, n, value_type="pv", due=False):
    """
    Source: lecture02/lecture02.ipynb.

    Merged from pv_annuity, fv_annuity, pv_annuity_due, fv_annuity_due.
    Computes present value or future value of an ordinary annuity or annuity due.
    """
    if value_type == "pv":
        value = c * (1 - (1 + r) ** -n) / r
    elif value_type == "fv":
        value = c * ((1 + r) ** n - 1) / r
    else:
        raise ValueError("value_type must be 'pv' or 'fv'")

    return value * (1 + r) if due else value


def growing_annuity_value(c, r, g, n, value_type="pv", due=False):
    """
    Source: lecture02/lecture02.ipynb.

    Merged from pv_growing_annuity, fv_growing_annuity,
    pv_growing_annuity_due, fv_growing_annuity_due.
    Computes present value or future value of a growing annuity.
    """
    if value_type == "pv":
        if r == g:
            value = c * n / (1 + r)
        else:
            value = c / (r - g) * (1 - ((1 + g) / (1 + r)) ** n)
    elif value_type == "fv":
        if r == g:
            value = c * n * (1 + r) ** (n - 1)
        else:
            value = c * ((1 + r) ** n - (1 + g) ** n) / (r - g)
    else:
        raise ValueError("value_type must be 'pv' or 'fv'")

    return value * (1 + r) if due else value


def perpetuity_value(c, r, g=0, due=False, delay=0):
    """
    Source: lecture02/lecture02.ipynb.

    Merged from pv_perpetuity, pv_perpetuity_due, pv_growing_perpetuity,
    pv_growing_perpetuity_due, pv_perpetuity_delayed,
    pv_growing_perpetuity_delayed.
    Computes present value of ordinary, due, growing, and delayed perpetuities.
    """
    if g == 0:
        value = c / r
    else:
        value = c / (r - g)

    if due:
        value *= 1 + r
    if delay:
        value /= (1 + r) ** delay

    return value


def effective_annual_rate(apr, nper):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: effect.
    Computes the effective annual rate from APR and compounding frequency.
    """
    return (1 + apr / nper) ** nper - 1


def convert_compounding_frequency(apr1, fre1, fre2):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: effcetiverates.
    Converts a rate compounded at fre1 into an equivalent per-period rate at fre2.
    """
    return (1 + apr1 / fre1) ** (fre1 / fre2) - 1


def nominal_to_continuous_rate(rm, fre):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: rmtorc.
    Converts a nominal periodic rate to a continuously compounded rate.
    """
    return fre * log(1 + rm)


def future_value_continuous(pv, rc, t):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: fv_continuous.
    Computes future value under continuous compounding.
    """
    return pv * exp(rc * t)
