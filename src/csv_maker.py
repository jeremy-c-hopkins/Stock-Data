import requests
import pandas as pd
import yfinance as yf
import urllib.request

from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def format_currency(amount):
    return "${:,.2f}".format(amount)


small_cap = pd.read_csv(
    "/home/bread/Coding/Finance/src/data/small_cap.csv", index_col=False
)

stocks = list(small_cap["Symbol"])

print(yf.Ticker(stocks[3]).info.keys())

stocks = stocks[:20]

ticker = []
sector = []
industry = []
industry_key = []
market_cap = []
enterprise = []
ebitda = []

#enterprise ratio < industry average suggests underpriced
enterprise_ratio = []

#high indicates overvalue
forward_pe = []
trailing_pe = []

risk = []
quick_ratio =  []

#peg < 1.0 suggests underprices
peg = []

stock_info = {
    'Ticker': ticker,
    'Sector': sector,
    'Industry': industry,
    'Industry Key': industry_key,
    'Market Cap': market_cap,
    'Enterprise Value': enterprise,
    'EBITDA': ebitda,
    'Enterprise Ratio': enterprise_ratio,
    'Forward PE': forward_pe,
    'Trailing PE': trailing_pe,
    'Overall Risk': risk,
    'Quick Ratio': quick_ratio,
    'PEG Ratio': peg
}

for stock in stocks:
    temp = yf.Ticker(stock)
    try:
        info_list = [
            temp.info['sector'],
            temp.info['industry'],
            temp.info['industryKey'],
            temp.info['marketCap'],
            temp.info['enterpriseValue'],
            temp.info['ebitda'],
            temp.info['enterpriseToEbitda'],
            temp.info['trailingPE'],
            temp.info['forwardPE'],
            temp.info['overallRisk'],
            temp.info['quickRatio'],
            temp.info['trailingPegRatio']
        ]
        ticker.append(stock)
        sector.append(info_list[0])
        industry.append(info_list[1])
        industry_key.append(info_list[2])
        market_cap.append(info_list[3])
        enterprise.append(info_list[4])
        ebitda.append(info_list[5])
        enterprise_ratio.append(info_list[6])
        trailing_pe.append(info_list[7])
        forward_pe.append(info_list[8])
        risk.append(info_list[9])
        quick_ratio.append(info_list[10])
        peg.append(info_list[11])
    except:
        continue

data = pd.DataFrame(stock_info)
data.to_excel("~/test.ods", index=False)
print(data)
