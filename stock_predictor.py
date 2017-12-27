import quandl
import numpy as np
import pandas as pd
import pickle

# Get all stock prices
comp_names = pd.read_csv("NSE_Company_Symbols.csv", encoding="latin1")
comp_sym = comp_names["SYMBOL"].values

stock_prices_dict = {'symbol': 'prices'}
for i in range(0,len(comp_sym)):
    try:
        stock_prices_dict[comp_sym[i]] = quandl.get("NSE/"+comp_sym[i], authtoken="issrQsEoPfrk4LmavLmi")
        print(i)
    except:
        pass
with open('stock_prices_dict.pickle', 'wb') as f:
    pickle.dump(stock_prices_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

# Load data (deserialize)
with open('stock_prices_dict.pickle', 'rb') as f:
    stock_prices_dict = pickle.load(f)
for key,val in stock_prices_dict.items():
    print(key)

# Get stock data for NSE 50 stocks
nse_50 = pd.read_csv("nse_50.csv")
nse_50 = nse_50["Symbol"].values

nse_50_stock_data = {k:v for k,v in stock_prices_dict.items() if k in nse_50}
with open('nse_50_stock_data.pickle', 'wb') as f:
    pickle.dump(nse_50_stock_data, f, protocol=pickle.HIGHEST_PROTOCOL)



# Extracting stock prices for Wipro
historical_stock_price = stock_prices_dict["WIPRO"]
historical_stock_price.head()
del stock_prices_dict
historical_stock_price.tail(1)

# Extract closing prices
closing_prices = historical_stock_price.loc[:,"Close"].values
len(closing_prices)

# Create training data

lag_prices = []
for i in range(6,len(closing_prices)):
    lag_prices.append(closing_prices[(i-6):i])

features = pd.DataFrame(lag_prices)
features.reset_index(drop=True,inplace=True)
features.columns = list(map(lambda x:'t-'+ str(x),[6,5,4,3,2,1]))


train_df = pd.DataFrame({"target_var": closing_prices[6:]})
train_df.reset_index(drop=True,inplace=True)
train_df = pd.concat([features,train_df], axis=1)
train_df.shape

# Convert raw scores to percentages
perct_changes = train_df.apply(lambda x: [100.0 * a1 / a2 - 100 for a1, a2 in zip(x[1:], x)], axis = 1)
perct_changes = list(map(lambda x: list(x), perct_changes))
perct_changes = pd.DataFrame(perct_changes)
perct_changes.columns = ["t-5","t-4","t-3","t-2","t-1","target_var"]

# Convert percent change to category
# compute percentile change quantiles
daily_perct_change = [100.0 * a1 / a2 - 100 for a1, a2 in zip(closing_prices[1:], closing_prices)]

percentiles = list(map(lambda x:np.nanpercentile(np.array(daily_perct_change),q = x),
                       [20,40,60,80]))


def change_perct_change_to_cat(raw_perct_change,percentiles):
    category = np.where(raw_perct_change < percentiles[0], "Cat1",
                        np.where(raw_perct_change < percentiles[1],"Cat2",
                                 np.where(raw_perct_change < percentiles[2], "Cat3",
                                          np.where(raw_perct_change < percentiles[3], "Cat4","Cat5"))))
    return category

# Check function
change_perct_change_to_cat(-1,percentiles)

# Apply function on all columns
perct_changes_cat = perct_changes.apply(lambda x: change_perct_change_to_cat(x,percentiles), axis=1)


