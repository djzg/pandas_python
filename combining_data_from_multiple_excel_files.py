#  Combining Data From Multiple Excel Files
# https://pbpython.com/excel-file-combine.html

import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', 15)


glob.glob('sales*.xlsx')

# Initialize a blank Dataframe then append all individual files into the all_data Dataframe
all_data = pd.DataFrame()

for f in glob.glob('sales*.xlsx'):
    df = pd.read_excel(f)
    all_data = all_data.append(df, ignore_index=True)

print(all_data.describe())
print(all_data.head())

all_data['date'] = pd.to_datetime(all_data['date'])


# Combining data

# Read in another file that contains the customer status by account

status = pd.read_excel('customer-status.xlsx')
print(status)

# Merging data with concatenated data set of sales using merge function
all_data_st = pd.merge(all_data, status, how='left')
print(all_data_st.head())

print(all_data_st[all_data_st["account number"] == 737550].head())

# Label all missing accounts as bronze using fillna function
all_data_st['status'].fillna('bronze', inplace=True)
print(all_data_st.head())

print(all_data_st[all_data_st["account number"] == 737550].head())


# Using categories

# First, typecast it to the column to a category using astype()
all_data_st['status'] = all_data_st['status'].astype('category')

print(all_data_st.dtypes)

# Sorting categories alphabetically
all_data_st.sort_values(by=["status"]).head()
print(all_data_st.head())

# Use set_categories to tell the order we want to use for this category object.
all_data_st["status"].cat.set_categories(["gold", "silver", "bronze"], inplace=True)
print(all_data_st.head())
print(all_data_st.sort_values(by=["status"]).head())


# Analyze data

print(all_data_st['status'].describe())

# Looking at how top customers performing compared to the bottom using groupby function
print(all_data_st.groupby(['status'])[['quantity', 'unit price', 'ext price']].mean())

# Running multiple aggregation functions on the data
print(all_data_st.groupby(['status'])[['quantity', 'unit price', 'ext price']].agg([np.sum, np.mean, np.std]))


# Filter out unique accounts and see how many gold, silver and bronze customers there are.
print(all_data_st.drop_duplicates(subset=['account number', 'name']).iloc[:, [0, 1, 7]].groupby(['status'])['name'].count())