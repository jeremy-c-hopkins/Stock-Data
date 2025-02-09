import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter

from datetime import datetime

date_format = "%Y-%m-%d"

pd.set_option("display.max_columns", None)

# def dollar_formatter(x, pos):
#     return f'${x:,.0f}'  # Formats with $ and 2 decimal places

# class RentalData():

#     def __init__(self, city):
#         self.csv = pd.read_csv('data/Metro_sales_count_now_uc_sfrcondo_month.csv')
#         self.locations = list(self.csv['Metro'].dropna())
#         self.cities = [place.split(',')[0].strip() for place in self.locations]

#         self.desired_city = city

#     def seach(self):

#         indices = [i for i, x in enumerate(self.cities) if x == self.desired_city]

#         self.data = [self.locations[i] for i in indices]

#         cost = self.csv.iloc[[indices[0]]].values[0]
#         dates = list(self.csv.iloc[[indices[0]]])

#         self.cost = list(cost[8:])
#         self.dates = dates[8:]

#     def data(self):

#         start = datetime.strptime(self.dates[0], date_format)
#         end = datetime.strptime(self.dates[-1], date_format)

#         self.timedelta = (end - start).days

#     def plot(self):

#         x = list(range(len(self.cost)))

#         coef = np.polyfit(x, self.cost, 1)
#         poly1d_fn = np.poly1d(coef)

#         fit = linregress(x, self.cost)

#         plt.plot(self.dates, self.cost, x, poly1d_fn(x), '--k')

#         plt.xlabel("Dates")
#         plt.ylabel("Cost")
#         plt.xticks(rotation=40)

#         plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=18))  # Adjust 'nbins' to control tick density
#         plt.gca().yaxis.set_major_formatter(FuncFormatter(dollar_formatter))

#         plt.title(f"Rent Price in {self.desired_city} Through Time")
#         plt.tight_layout()  # Ensures everything fits within the figure
#         plt.show()

#         return fit

# search = "Salt Lake City"

# rent = RentalData(search)

# rent.seach()
# rent.plot()

desired_city = "Salt Lake City"

csv = pd.read_csv("src/data/Metro_sales_count_now_uc_sfrcondo_month.csv")

locations = list(csv["RegionName"].dropna())

cities = [place.split(",")[0].strip() for place in locations]

indices = [i for i, x in enumerate(cities) if x == desired_city]

data = [locations[i] for i in indices]

print(data)

# locations = list(csv['Metro'].dropna())
# cities = [place.split(',')[0].strip() for place in locations]
