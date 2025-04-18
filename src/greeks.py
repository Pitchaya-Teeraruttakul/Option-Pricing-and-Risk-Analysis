import numpy as np
from binomial import binomial


def greeks(S, K, T, q, ot, sigma, dS=0.01, dVol=0.01, dT=1 / 365):
    """
    Parameters:
    - sigma: implied volatility
    - q: dividend yield
    - ot: option type
    - dS: small change in spot price
    - dVol: small change in volatility
    - dT: small change in time (default 1 day)

    """

    basePrice = binomial(S, K, T, q, ot, sigma)
    priceUp = binomial(S + dS, K, T, q, ot, sigma)
    priceDown = binomial(S - dS, K, T, q, ot, sigma)

    # Delta: change in option price when spot price changes
    delta = (priceUp - priceDown) / (dS * 2)

    # Gamma: change in option Delta when spot price changes
    gamma = (priceUp - 2 * basePrice + priceDown) / (dS**2)

    # Theta: change in price over time
    if T - dT > 0:
        shorter = binomial(S, K, T - dT, q, ot, sigma)
        theta = (shorter - basePrice) / dT
    else:
        theta = float("NA")  # Not defined for negative time

    # Vega: sensitivity to volatility
    priceHVol = binomial(S, K, T, q, ot, sigma + dVol)
    priceLVol = binomial(S, K, T, q, ot, sigma - dVol)
    vega = (priceHVol - priceLVol) / (2 * dVol)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "modelPrice": basePrice,
    }
