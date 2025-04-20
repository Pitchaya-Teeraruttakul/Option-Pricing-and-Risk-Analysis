import os
import numpy as np
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))
# riskFreeRate = (
#     fred.get_series("GS1M").tail(1).values[0] / 100
# )  # GS1M treasury Constant Maturity 1 Month (get last month March 2025)
riskFreeRate = 0.0436


# N need to be tune as # of trading day but let's set to constant = 100 (100 steps of binomial)
def binomial(S, K, T, q, ot, sigma, N=100, r=riskFreeRate):
    # specify input parameters
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))  # up factor
    d = 1 / u  # down factor
    p = (np.exp((r - q) * dt) - d) / (u - d)  # risk neutral prob
    discountFactor = np.exp(-r * dt)  # discount factor calculate from risk free rate

    # build stock or ETF price tree
    stree = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(N + 1):
            stree[j, i] = S * (u ** (i - j)) * (d**j)
    # value of option at maturity
    otree = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        if ot == "call":
            otree[j, N] = max(stree[j, N] - K, 0)
        else:
            otree[j, N] = max(K - stree[j, N], 0)

    # backward
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            h = discountFactor * (p * otree[j, i + 1] + (1 - p) * otree[j + 1, i + 1])
            if ot == "call":
                ex = max(stree[j, i] - K, 0)
            else:
                ex = max(K - stree[j, i], 0)
            otree[j, i] = max(h, ex)

    return otree[0, 0]
