import pickle
import stockstats
# Load data (deserialize)
with open('stock_prices_dict.pickle', 'rb') as f:
    stock_prices_dict = pickle.load(f)

df = stock_prices_dict["WIPRO"]
df_stock = StockDataFrame.retype(df)