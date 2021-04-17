#  Common Excel Tasks Demonstrated in Pandas - Part 2
#  https://pbpython.com/excel-pandas-comp-2.html

import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 15)


df = pd.read_excel("sample-salesv3.xlsx")
print(df.dtypes)

df['date'] = pd.to_datetime(df['date'])
print(df.head())
print(df.dtypes)

# Filtering the data

print(df[df['account number'] == 307599].head())
print(df[df['quantity'] > 22].head())

# Filtering data using map function
# Looking for items with 'sku's that start with B1
print(df[df['sku'].map(lambda x: x.startswith('B1'))].head())

# Chaining more statements with &
print(df[df['sku'].map(lambda x: x.startswith('B1')) & (df['quantity'] > 22)].head())

# Using isin function
print(df[df['account number'].isin([714466, 218895])].head())

# Using query function. Requires numexpr module
print(df.query('name == ["Kulas Inc","Barton LLC"]').head())


# Working with dates
# Before doing anything with dates, sort by date to make sure results expected return
df = df.sort_values(by=['date'])
print(df.head())


print(df[df['date'] >= '20140905'].head())
print(df[df['date'] >= '2014-03'].head())
print(df[(df['date'] >= '20140701') & (df['date'] <= '20140715')].head())
print(df[df['date'] >= 'Oct-2014'].head())
print(df[df['date'] >= '10-10-2014'].head())

# When working with time series data, if we convert the data to use the date as the index, we can do some more filtering
# variations

df2 = df.set_index(['date'])
print(df2.head())

# Slicing data to get the range
print(df2["20140101":"20140201"].head())
print(df2["2014-Jan-1":"2014-Feb-1"].head())
print(df2["2014-Jan-1":"2014-Feb-1"].tail())
print(df2["2014-Dec"].head())


# Additional string functions
# str.contains and sort
print(df[df['sku'].str.contains('B1')].head())
print(df[(df['sku'].str.contains('B1-531')) & (df['quantity'] > 40)].sort_values(by=['quantity', 'name'], ascending=[0, 1]))

# Finding a list of unique items in a long list
print(df['name'].unique())

# Using drop_duplicates()
print(df.drop_duplicates(subset=['account number', 'name']).head())

# Select only the first and second columns using iloc()
print(df.drop_duplicates(subset=['account number', 'name']).iloc[:, [0, 1]])


