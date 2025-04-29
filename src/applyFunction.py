import pandas as pd
from binomial import binomial
from IPython.display import display

nvda = pd.read_csv("data/cleaned_options_nvda.csv")
spy = pd.read_csv("data/cleaned_options_spy.csv")

nvdaResult = []
spyResult = []

nvda["modelPrice"] = nvda.apply(
    lambda r: binomial(
        S=r["spot"],
        K=r["strike"],
        T=r["ttm"],
        q=r["dividendYield"],
        ot=r["type"],
        sigma=r["impliedVolatility"],
    ),
    axis=1,
)

spy["modelPrice"] = spy.apply(
    lambda r: binomial(
        S=r["spot"],
        K=r["strike"],
        T=r["ttm"],
        q=r["dividendYield"],
        ot=r["type"],
        sigma=r["impliedVolatility"],
    ),
    axis=1,
)

display(nvda)
nvda.to_csv("data/cleanedNVDA.csv", index=False)
display(spy)
spy.to_csv("data/cleanedSPY.csv", index=False)
