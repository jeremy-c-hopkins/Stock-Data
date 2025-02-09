import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter

from datetime import datetime
from dataclasses import dataclass

date_format = "%Y-%m-%d"

pd.set_option("display.max_columns", None)


def dollar_formatter(x, pos):
    return f"${x:,.0f}"  # Formats with $ and 2 decimal places


@dataclass
class CSVFiles:
    city: str = "Salt Lake City"
    rental_price: str = "City_zori_uc_sfrcondomfr_sm_month.csv"
    housing_sale_count: str = "Metro_sales_count_now_uc_sfrcondo_month.csv"


class HousingData:

    def __init__(self, args):
        self.csv = pd.read_csv("City_zori_uc_sfrcondomfr_sm_month.csv")
        self.locations = list(self.csv["Metro"].dropna())
        self.cities = [place.split(",")[0].strip() for place in self.locations]

        self.desired_city = city

    def search(self):

        indices = [i for i, x in enumerate(self.cities) if x == self.desired_city]

        self.data = [self.locations[i] for i in indices]

        cost = self.csv.iloc[[indices[0]]].values[0]
        dates = list(self.csv.iloc[[indices[0]]])

        self.cost = list(cost[8:])
        self.dates = dates[8:]

    def data(self):

        start = datetime.strptime(self.dates[0], date_format)
        end = datetime.strptime(self.dates[-1], date_format)

        self.timedelta = (end - start).days

    def plot(self):

        x = list(range(len(self.cost)))

        coef = np.polyfit(x, self.cost, 1)
        poly1d_fn = np.poly1d(coef)

        fit = linregress(x, self.cost)

        plt.plot(self.dates, self.cost, x, poly1d_fn(x), "--k")

        plt.xlabel("Dates")
        plt.ylabel("Cost")
        plt.xticks(rotation=40)

        plt.gca().xaxis.set_major_locator(
            MaxNLocator(nbins=18)
        )  # Adjust 'nbins' to control tick density
        plt.gca().yaxis.set_major_formatter(FuncFormatter(dollar_formatter))

        plt.title(f"Rent Price in {self.desired_city} Through Time")
        plt.tight_layout()  # Ensures everything fits within the figure
        plt.show()

        return fit


search = "Salt Lake City"

rent = HousingData(search)

rent.search()
rent.plot()
