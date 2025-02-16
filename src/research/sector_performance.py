#Work on plotting performance by quarter by sector

import yfinance as yf
from utils import constants as c

sectors = [yf.Sector(sector) for sector in c.sectors]
print(sectors)
# tech = yf.Sector("basic-materials")
# print(tech.ticker.ticker)

# stock = yf.Ticker("msft")
# print(stock.upgrades_downgrades)