import numpy as np
import pandas as pd
import yfinance as yf

from scipy.stats import norm
from scipy.integrate import quad
from datetime import datetime, timedelta

def cdf(t):
    return 1/np.sqrt(2 * np.pi) * np.exp((-t**2)/2)

class OptionsMetrics():

    def __init__(self, ticker, option, strike, t):
        self.stock = yf.Ticker(ticker)
        self.option = option
        self.strike = strike
        self.t = t

        self._get_days()
        self._get_data()
        self._sigma()
        self._risk_free()
        self._d1()
        self._d2()

    def _get_days(self):
        today =  datetime.now()
        self.start =  (today -  timedelta(days=120)).strftime("%Y-%m-%d")
        self.end = today.strftime("%Y-%m-%d")

        self.weekdays = pd.date_range(
            start=pd.to_datetime(self.start) + pd.Timedelta('1 days'),
            end=pd.to_datetime(self.end)
        ).to_series().map(lambda x: 1 if x.isoweekday() in range(1, 6) else 0).sum()

    def _get_data(self):
        data = self.stock.history(period='6mo')
        self.data = data.iloc[::-1].iloc[:self.weekdays]
        self.price = self.data["Close"].iloc[0]

    def _sigma(self):
        log_returns = np.log(self.data["Close"]/(self.data["Close"].shift(1)))
        log_returns = log_returns.dropna()
        self.sigma = np.std(log_returns) * np.sqrt(252)

    def _risk_free(self):
        self.r = 0.043

    def _d1(self):
        self.d1 = (np.log(self.price / self.strike) + (self.r + (self.sigma**2)/2) *  self.t) / (self.sigma * np.sqrt(self.t))
    
    def _d2(self):
        self.d2 = self.d1 - self.sigma * np.sqrt(self.t)

    def _cdf(self, d):
        return quad(cdf, -np.inf, d)

    def option_value(self):
        if self.option.lower() ==  "call":
            N_d1 = norm.cdf(self.d1)
            N_d2 = norm.cdf(self.d2)
            value = self.price * N_d1 - self.strike * np.exp(- self.r * self.t) * N_d2
            return value
    

option = OptionsMetrics("AAPL", "call", 230, 120/365)

print(f"${option.option_value():.2f}")

# from scipy.integrate import quad

# I = quad(cdf, -np.inf, option.d1)
# print(I)