import time
import decimal
import requests
import warnings
import pandas as pd
import yfinance as yf
from lxml import html
import constants as c
import functions as f
from functools import lru_cache

from babel import numbers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')

import requests_cache
session = requests_cache.CachedSession('yf.cache')
session.headers['User-agent'] = 'my-program/1.0'

warnings.filterwarnings('ignore')
start_time = time.time()

# Using wrapper to check method arguments
def check(allowed, type_check):
    def wrapper(method):
        def inner(self, *args, **kwargs):
            if(type_check == "market"):
                if self.market not in allowed:
                    raise ValueError("Method not available for market '{}'. Allowed markets: {}".format(self.market, ", ".join(allowed)))
            return method(self, *args, **kwargs)
        return inner
    return wrapper


class DataScraping():

    def __init__(self, ticker, market="stock"):
        
        self.ticker = ticker.lower()
        self.market = market

        # Changing scrape site based on market type
        if isinstance(ticker, list):
            self.link = ['https://www.marketwatch.com/investing/stock/{}/analystestimates'.format(ticker) for ticker in self.ticker]
        else:
            self.link = "https://www.marketwatch.com/investing/stock/{}/analystestimates".format(self.ticker)


    
    def get_industry_leaders(self):
        """
        Gets a list of the top stocks from industry of ticker provided to the class. 

        :returns: top stocks
        :rtype: dataframe
        """
        temp = yf.Ticker(self.ticker)
        industry = temp.info['industryKey']
        industry_leaders = yf.Industry(industry).top_companies

        return industry_leaders


    def parse_volume(self, volume_str):
        return int(float(volume_str.rstrip('M')) * 1_000_000) if volume_str.endswith('M') else int(volume_str)

    
    def get_volume_leaders(self):
        """
        Gets stocks that had the highest trade volume for today.

        :returns: list of stocks and their associated volume
        :rtype: list of strings
        """
        url = requests.get("https://finance.yahoo.com/markets/stocks/most-active/")
        print(url)
        info = html.fromstring(url.content)
        print(info)
        leaders = [info.xpath(f"/html/body/div[2]/main/section/section/section/article/section[1]/div/div[2]/div/table/tbody/tr[{i}]/td[1]/span/div/a/div/span/text()")[0] for i in range(1, 26)]
        volume = [self.parse_volume(info.xpath(f"/html/body/div[2]/main/section/section/section/article/section[1]/div/div[2]/div/table/tbody/tr[{i}]/td[7]/span/fin-streamer/text()")[0]) for i in range(1, 26)]
        return (leaders, volume)

    
    @check(["stock"], "market")
    def get_stock_rating(self):
        """
        Gets most common analyst rating for given stock. This is averaged across all ratings. If a
        list of stocks is passed then a dataframe will be returned, otherwise just a string.

        :return: rating (overweight, underweight, buy, sell, hold)
        :rtype: string or dataframe
        :raises ValueError: if self.market is not "stock"
        """

        if len(self.ticker) == 1:
            url = requests.get(self.links[0])
            info = html.fromstring(url.content)
            rating = info.xpath('/html/body/div[3]/div[6]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]/text()')[0]
            return rating

        df = pd.DataFrame()
        ratings = []
        df["Stocks"] = self.ticker
        for link in self.links:
            url = requests.get(link)
            info = html.fromstring(url.content)
            rating = info.xpath('/html/body/div[3]/div[6]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]/text()')[0]
            ratings.append(rating)

        df["Rating"] = ratings
        return df

    
    @check(["stock"], "market")
    def get_stock_target(self):
        """
        Gets most common analyst price target for given stock. This is averaged across all targets.
        If a list of stocks is passed then a dataframe will be returned, otherwise just an int. The
        dataframe will also contain the stocks current price.

        :return: price target
        :rtype: int or dataframe
        :raises ValueError: if self.market is not "stock"
        """

        if (len(self.link) == 1):
            url = requests.get(self.link[0])
            info = html.fromstring(url.content)
            target = info.xpath('/html/body/div[3]/div[6]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]/text()')[0]
            return target

        df = pd.DataFrame()
        df["Stocks"] = self.tickers

        targets = []
        current_price = []
        for link in self.links:
            url = requests.get(link)
            info = html.fromstring(url.content)
            target = info.xpath('/html/body/div[3]/div[6]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]/text()')[0]
            targets.append(target)
            price  = info.xpath('/html/body/div[3]/div[1]/div[3]/div/div[2]/h2/bg-quote/text()')[0]
            current_price.append(price)

        df["Target"] = targets
        df["Current Price"] = current_price
        return df


    @check(["fund"], "market")
    def get_fund_holdings(self):
        """
        Gets a list of all holdings maintained by the given etf.

        :return: fund holdings
        :rtype: list of strings
        """
        url = requests.get(self.links[0])
        info = html.fromstring(url.content)

        target = [info.xpath(f"/html/body/div[3]/div[6]/div[3]/div/table/tbody/tr[{i}]/td[2]/text()")[0] for i in range(1, 50) if len(info.xpath(f"/html/body/div[3]/div[6]/div[3]/div/table/tbody/tr[{i}]/td[2]/text()"))>0]
        return target


    def get_financials(self):
        """
        Gets multiple Pandas dataframes for financial metrics

        :return: financials
        :rtype: list of pandas dataframes
        """

        dataLinks = [
            f"https://stockanalysis.com/stocks/{self.ticker}/financials/", 
            f"https://stockanalysis.com/stocks/{self.ticker}/financials/balance-sheet/", #/html/body/div/div[1]/div[2]/main/div[2]/nav[1]/ul/li[2]
            f"https://stockanalysis.com/stocks/{self.ticker}/financials/cash-flow-statement/", 
            f"https://stockanalysis.com/stocks/{self.ticker}/financials/ratios/"
        ]

        driver = webdriver.Chrome(options=chrome_options)

        data = []

        for link in dataLinks:

            try:
                driver.get(link)

                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/main/div[4]/table/tbody")))

                rows = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div[2]/main/div[4]/table/tbody/tr")
                header_row = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/main/div[4]/table/thead/tr[2]")
                headers = [header.text for header in header_row.find_elements(By.TAG_NAME, "th")]
                temp = [headers]

                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    temp.append([column.text for column in columns])

                data.append(temp)
            except TimeoutError:
                print(f"Timeout while waiting for {link}")
                continue

        driver.quit()

        financials = pd.DataFrame(data[0])
        headers = financials.iloc[0]
        financials.columns = [headers]
        financials.drop(index=0, axis=0, inplace=True)

        balanceSheet = pd.DataFrame(data[1])
        headers = balanceSheet.iloc[0]
        balanceSheet.columns = [headers]
        balanceSheet.drop(index=0, axis=0, inplace=True)

        cashFlow = pd.DataFrame(data[2])
        headers = cashFlow.iloc[0]
        cashFlow.columns = [headers]
        cashFlow.drop(index=0, axis=0, inplace=True)

        ratios = pd.DataFrame(data[3])
        headers = ratios.iloc[0]
        ratios.columns = [headers]
        ratios.drop(index=0, axis=0, inplace=True)

        financials.rename(columns={'Period Ending':'Markers'})
        balanceSheet.rename(columns={'Period Ending':'Markers'})
        cashFlow.rename(columns={'Period Ending':'Markers'})
        ratios.rename(columns={'Period Ending':'Markers'})

        return(financials, balanceSheet, cashFlow, ratios)

    
def open_insider(ticker):
    """
    Gets information from openinsider.com on stock

    :return: list of every insider purchase and sale recorded through the sec 13d
    :rtype: pandas dataframe
    """

    link = f"http://openinsider.com/search?q={ticker}"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(link)
    driver.implicitly_wait(10)  

    page_source = driver.page_source
    info = html.fromstring(page_source)

    rows = info.xpath('/html/body/div[2]/table/tbody/tr')

    table_data = []

    for row in rows:

        columns = row.xpath('.//td')
        row_data = [column.text_content().strip() for column in columns]
        table_data.append(row_data)

    driver.quit()

    if len(table_data) == 0:
        return

    df = pd.DataFrame(table_data)

    df = df.drop([12, 13, 14, 15], axis=1)

    df = df.rename(columns={
        0: "Filing Type", 
        1: "Filing Date", 
        2: "Trade Date", 
        3: "Ticker", 
        4: "Insider Name", 
        5: "Title", 
        6: "Trade Type", 
        7: "Price", 
        8: "Quantity", 
        9: "Owned", 
        10: "Delta Own", 
        11: "Value"
    })

    df["Value"] = f.parse_str_value(df, "Value")
    df["Price"] = f.parse_str_value(df, "Price")
    df["Quantity"] = f.parse_str_value(df, "Quantity")

    return df, link

        
small_cap = pd.read_csv("/home/bread/Coding/Finance/src/data/market_cap/small_cap.csv")
tickers = list(small_cap["Symbol"])
tickers = tickers[500:550]

for ticker in tickers:
    try:
        temp, link = open_insider(ticker)
        if temp is not None:
            sum_value = sum(list(temp["Value"]))
            if sum_value > 0:
                print(ticker, link, numbers.format_currency(sum_value, 'USD'))
    except:
        continue
    


 
end_time = time.time()
execution_time = end_time - start_time
print(f"The code ran in: {execution_time:.3f}s")
