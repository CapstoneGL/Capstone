
import pickle
import pandas as pd
from stockstats import StockDataFrame
# Load data (deserialize)
with open('nse_50_stock_data.pickle', 'rb') as f:
    stock_prices_dict = pickle.load(f)

df = stock_prices_dict["ABB"]
df = StockDataFrame.retype(df)

tech_indicators = ["kdjk","macd","rsi_6","rsi_12",
                   "wr_10","wr_6","cci","adx","mdi"]
tech_indicators_df = list(map(lambda x: df[x], tech_indicators))
tech_indicators_df = pd.DataFrame(tech_indicators_df).transpose()

stock_df = pd.concat([df[["close"]],tech_indicators_df],axis=1)

stock_df.to_clipboard()

[keys for keys,vals in stock_prices_dict.items]
import os

