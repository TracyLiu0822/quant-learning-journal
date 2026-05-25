"""Fixed income valuation and duration utilities."""


def _financial_pv(rate, nper, pmt, fv):
    """
    Source: lecture04/lecture04.ipynb.

    Internal helper derived from the numpy_financial.pv logic used by bond_price,
    zero_price, and duration in the original lecture.
    """
    if rate == 0:
        return -(fv + pmt * nper)
    return -(pmt * (1 - (1 + rate) ** -nper) / rate + fv / (1 + rate) ** nper)


def _financial_rate(nper, pmt, pv, fv, low=-0.9999, high=1.0, tol=1e-10, max_iter=200):
    """
    Source: lecture04/lecture04.ipynb.

    Internal helper derived from the numpy_financial.rate logic used by bond_ytm
    in the original lecture.
    """
    def value(rate):
        if rate == 0:
            return pv + pmt * nper + fv
        return pv + pmt * (1 - (1 + rate) ** -nper) / rate + fv / (1 + rate) ** nper

    f_low = value(low)
    f_high = value(high)

    while f_low * f_high > 0 and high < 100:
        high *= 2
        f_high = value(high)

    if f_low * f_high > 0:
        raise ValueError("Could not bracket a rate solution")

    for _ in range(max_iter):
        mid = (low + high) / 2
        f_mid = value(mid)
        if abs(f_mid) < tol:
            return mid
        if f_low * f_mid <= 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid

    return (low + high) / 2


def bond_price(fv, ytm, couponrate=0, year=1, fre=1):
    """
    Source: lecture04/lecture04.ipynb.

    Merged duplicate bond_price definitions from cell 1 and cell 2.
    Computes coupon bond price; set couponrate=0 for a zero coupon bond.
    """
    rate = ytm / fre
    nper = year * fre
    pmt = fv * couponrate / fre
    return _financial_pv(rate, nper, pmt, fv)


def zero_coupon_bond_price(fv, rate, year):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: zero_price.
    Computes zero coupon bond price.
    """
    return _financial_pv(rate, year, 0, fv)


def bond_ytm(pv, fv, couponrate, year, fre):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: bond_ytm.
    Computes annualized yield to maturity.
    """
    nper = year * fre
    pmt = fv * couponrate / fre
    return _financial_rate(nper, pmt, pv, fv) * fre


def macaulay_duration(year, fv, rate, couponrate, fre):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: duration.
    Computes Macaulay duration.
    """
    nper = year * fre
    coupon = fv * couponrate / fre
    price = bond_price(fv, rate, couponrate, year, fre)
    duration_value = 0

    for i in range(1, nper + 1):
        t = i / fre
        cf = coupon if i < nper else coupon + fv
        pv_cf = _financial_pv(rate / fre, i, 0, cf)
        duration_value += t * (pv_cf / price)

    return round(duration_value, 4)


def modified_duration(dur, ytm, fre):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: mod_d.
    Computes modified duration from Macaulay duration.
    """
    return dur / (1 + ytm / fre)


def plot_yield_curve(time, rate):
    """
    Source: lecture04/lecture04.ipynb.

    Original function: plot_yield.
    Plots a term structure curve.
    """
    import matplotlib.pyplot as plt

    plt.plot(time, rate)
    plt.xlabel("time")
    plt.ylabel("rate")
    plt.title("term structure")
    plt.show()
