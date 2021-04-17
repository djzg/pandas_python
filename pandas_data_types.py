#            Pandas Data Types
# https://pbpython.com/pandas_dtypes.html

import pandas as pd
import numpy as np

df = pd.read_csv("sales_data_types.csv")

# adding two columns concatenates two values
summed = df['2016'] + df['2017']
print(summed)

# listing all dataframe types
print(df.dtypes)

# more info
print(df.info)

"""
    The Customer Number is a float64 but it should be an int64
    The 2016 and 2017 columns are stored as objects, not numerical values such as a float64 or int64
    Percent Growth and Jan Units are also stored as objects not numerical values
    We have Month , Day and Year columns that should be converted to datetime64
    The Active column should be a boolean
"""

# Using astype() function

df["Customer Number"] = df['Customer Number'].astype('int')
print(df['Customer Number'].dtypes)

# astype() will only work if the data is clean and can be simply interpreted as number, and you want to convert a
# numeric value to a string object


# Custom conversion functions

# Currency conversion
def convert_currency(val):
    """
    Convert the string number value to a float
    - Remove $
    - Remove commas
    - Convert to a float type
    """
    new_val = val.replace(',', '').replace('$', '')
    return float(new_val)


df['2016'].apply(convert_currency)

# using lambda
df['2016'].apply(lambda x: x.replace('$', '').replace(',', '')).astype('float')

df['2016'] = df['2016'].apply(convert_currency)
df['2017'] = df['2017'].apply(convert_currency)

# Fixing Percent growth column

df['Percent Growth'].apply(lambda x: x.replace("%", "")).astype('float') / 100


# Using custom function
def convert_percent(val):
    """
    Convert the percentage string to an actual floating point percent
    - Remove %
    - Divide by 100 to make decimal
    """
    new_val = val.replace("%", "")
    return float(new_val) / 100


df['Percent Growth'] = df['Percent Growth'].apply(convert_percent)


# Using np.where() to convert all "Y" values to True and everything else to False

df["Active"] = np.where(df["Active"] == "Y", True, False)


# Pandas helper functions

# The reason the Jan Units conversion is problematic is the inclusion of a non-numeric value in the column
print(pd.to_numeric(df["Jan Units"], errors='coerce'))

# Value "Closed" is replaced with NaN that we can fill in with fillna(0):
df["Jan Units"] = pd.to_numeric(df["Jan Units"], errors='coerce').fillna(0)
print(pd.to_numeric(df["Jan Units"], errors='coerce').fillna(0))


# Converting the separate month, day and year into a datetime:
df['Start date'] = pd.to_datetime(df[['Day', 'Month', 'Year']])


# Using converter arguments
df_2 = pd.read_csv("sales_data_types.csv",
                   dtype={'Customer Number': 'int'},
                   converters={'2016': convert_currency,
                               '2017': convert_currency,
                               'Percent Growth': convert_percent,
                               'Jan Units': lambda x: pd.to_numeric(x, errors='coerce'),
                               'Active': lambda x: np.where(x == 'Y', True, False)
                               })
print(df_2.dtypes)