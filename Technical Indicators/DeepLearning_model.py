import numpy as np
import pandas as pd
import pickle
from stockstats import StockDataFrame

# Load dictionary of stock prices
with open('nse_50_stock_data.pickle', 'rb') as f:
    stock_prices_dict = pickle.load(f)

# Extracting stock prices for Wipro
historical_stock_price = stock_prices_dict["ABB"]
historical_stock_price.head()
historical_stock_price.shape

# Tech indicators
historical_stock_price = StockDataFrame.retype(historical_stock_price)
tech_indicators = ["kdjk","macd","rsi_6","rsi_12",
                   "wr_10","wr_6","cci","adx","mdi"]
tech_indicators_df = list(map(lambda x: historical_stock_price[x], tech_indicators))
tech_indicators_df = pd.DataFrame(tech_indicators_df).transpose()

stock_df = pd.concat([historical_stock_price[["close"]],tech_indicators_df],axis=1)
stock_df.head(3

# Extract data for last 1 year
stock_df["date"] = pd.to_datetime(stock_df.index)
stock_price_sub = stock_df[stock_df["date"] >= pd.to_datetime("2010-11-01")]

# Get closing day prices
closing_prices = stock_price_sub["close"].values
closing_prices[0:10]

# Previous day prices as features
# consider last 6 day prices
time_lag = 5
lag_prices = []
for i in range(time_lag,len(closing_prices)):
    lag_prices.append(closing_prices[(i-(time_lag)):i])

# Lag prices as features
features = pd.DataFrame(lag_prices)
features.reset_index(drop=True,inplace=True)
features.columns = list(map(lambda x:'t-'+ str(x),list(range(1,time_lag+1))))
features.head(3)