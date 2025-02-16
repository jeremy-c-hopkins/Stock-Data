import yfinance as yf
import pandas as pd

from itertools import islice  

class database():

    def __init__(self, portfolio_csv):

        self.portfolio_csv = portfolio_csv

        self.tickers = self.parse_csv()
        self.stocks = [yf.Ticker(ticker) for ticker in self.tickers]
        self.sectors = [yf.Sector(stock.info.get("sectorKey")) for stock in self.stocks]
        self.industries = [yf.Industry(stock.info.get("industryKey")) for stock in self.stocks]

        self._financials()

    def _financials(self):
        """
        Gets all financials including cash flow, balance sheet, income statement
        """
        income_stmt = [stock.income_stmt.iloc[:,0] for stock in self.stocks]
        self.income_stmt = [list(statement.values) for statement in income_stmt]
        self.income_stmt_index =  list(income_stmt[0].index)
        
        balance_sheet = [stock.balance_sheet.iloc[:,0] for stock in self.stocks]
        self.balance_sheet = [list(statement.values) for statement in balance_sheet]
        self.balance_sheet_index = list(balance_sheet[0].index)
        
        cash_flow = [stock.cashflow.iloc[:,0] for stock in self.stocks]
        self.cash_flow = [list(statement.values) for statement in cash_flow]
        self.cash_flow_index = list(cash_flow[0].index)

    def insert_positions(self):
        a

    def parse_csv(self):
        self.portfolio = pd.read_csv(self.portfolio_csv, index_col=False).dropna()
        return list(self.portfolio["Symbol"])
        

csv = "/home/bread/Downloads/Portfolio_Positions_Feb-12-2025.csv"
a = database(csv)

# ticker = yf.Ticker("AAPL")
# print(ticker.cashflow)