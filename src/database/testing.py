import sqlite3
import pandas as pd
import yfinance as yf

from itertools import islice  

class database():

    def __init__(self, portfolio_csv):

        self.portfolio_csv = portfolio_csv

        self.tickers = self.parse_csv()
        self.stocks = [yf.Ticker(ticker) for ticker in self.tickers]
        self.sectors = [yf.Sector(stock.info.get("sectorKey")) for stock in self.stocks]
        self.industries = [yf.Industry(stock.info.get("industryKey")) for stock in self.stocks]

        self.indices = []

        self._financials()

    def _financials(self):
        """
        Gets all financials including cash flow, balance sheet, income statement
        """

        income_stmt = [stock.income_stmt.fillna(-99999) for stock in self.stocks]
        print([len(statement.index) for statement in income_stmt])

        # income_stmt = [stock.income_stmt.fillna(0).iloc[:,0] for stock in self.stocks]
        # self.income_stmt = [list(statement.values) for statement in income_stmt]
        # self.indices.extend(list(income_stmt[0].index))
        
        # balance_sheet = [stock.balance_sheet.fillna(0).iloc[:,0] for stock in self.stocks]
        # self.balance_sheet = [list(statement.values) for statement in balance_sheet]
        # self.indices.extend(list(balance_sheet[0].index))
        
        # cash_flow = [stock.cashflow.fillna(0).iloc[:,0] for stock in self.stocks]
        # self.cash_flow = [list(statement.values) for statement in cash_flow]
        # self.indices.extend(list(cash_flow[0].index))

        # self.data = list(sub1 + sub2 + sub3 for sub1, sub2, sub3 in zip(self.income_stmt, self.balance_sheet, self.cash_flow))

        # print([len(self.data[i]) for i in range(len(self.data))])

    def insert_positions(self):
        table = f"""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                {", ".join(f'"{index}" REAL' for index in self.indices)}
            )
        """

        conn = sqlite3.connect("/home/bread/Coding/Stock-Data/src/database/portfolio.db")
        cursor = conn.cursor()

        cursor.execute(table)

        for data in self.data:
            print("hit")
            insert_sql = f'''
                INSERT INTO data ({", ".join(f'"{index}"' for index in self.indices)})
                VALUES ({", ".join("?" for _ in self.indices)})
            '''
            cursor.execute(insert_sql, data)

        conn.commit()
        conn.close()

    def parse_csv(self):
        self.portfolio = pd.read_csv(self.portfolio_csv, index_col=False).dropna()
        return list(self.portfolio["Symbol"])
        

csv = "/home/bread/Downloads/Portfolio_Positions_Feb-17-2025.csv"
a = database(csv)
# a.insert_positions()

# ticker = yf.Ticker("AAPL")
# print(ticker.cashflow)