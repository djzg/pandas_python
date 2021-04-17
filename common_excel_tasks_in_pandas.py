#  Common Excel Tasks Demonstrated in Pandas
# https://pbpython.com/excel-pandas-comp.html

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', 15)

df = pd.read_excel("excel-comp-data.xlsx")
print(df.head())


# Adding a Sum to row
df["Total"] = df["Jan"] + df["Feb"] + df["Mar"]
print(df.head())

df["Jan"].sum(), df["Jan"].mean(), df["Jan"].min(), df["Jan"].max()

# Adding a new row for sum values
sum_row = df[['Jan', 'Feb', 'Mar', 'Total']].sum()
print(sum_row)

# We need to transpose the data and convert the Series to a DataFrame so that it is easier to concat onto our
# existing data. The T function allows us to switch the data from being row-based to column-based.
df_sum = pd.DataFrame(data=sum_row).T
print(df_sum)

# Before adding totals back is to add the missing columns using reindex()
# Add all of our columns and then allow pandas to fill in the values that are missing
df_sum = df_sum.reindex(columns=df.columns)
print(df_sum)

# Now we add this dataframe to the existing one using append
df_final = df.append(df_sum, ignore_index=True)
print(df_final.tail())


# Additional data transforms
# Adding a state abbreviation to the data set

state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU",
                 "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI",
                 "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM",
                 "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL",
                 "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA",
                 "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM",
                 "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE",
                 "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA",
                 "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH",
                 "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA",
                 "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND",
                 "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI",
                 "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}

# Example how fuzzywuzzy text matching function works
print(process.extractOne("Minnesotta", choices=state_to_code.keys()))
print(process.extractOne("AlaBAMMazzz",choices=state_to_code.keys(),score_cutoff=80))


# Take the state column and convert it to a valid abbreviation using 80 as score_cutoff for this data


def convert_state(row):
    """
    return either valid abbreviation or np.nan
    """
    abbrev = process.extractOne(str(row["state"]), choices=state_to_code.keys(), score_cutoff=80)

    if abbrev:
        return state_to_code[abbrev[0]]
    return np.nan


# Adding column in the location we want and filling it with NaN values
df_final.insert(6, "abbrev", np.nan)
print(df_final)


# Using apply to add the abbreviations into the appropriate column
df_final['abbrev'] = df_final.apply(convert_state, axis=1)
print(df_final.tail())


# Subtotals using groupby()

df_sub = df_final[["abbrev", "Jan", "Feb", "Mar", "Total"]].groupby("abbrev").sum()
print(df_sub)


# Formatting data as currency using applymap to all the values in the data frame
def money(x):
    return "${:,.0f}".format(x)


formatted_df = df_sub.applymap(money)
print(formatted_df)
print("\n")

# Getting totals
sum_row = df_sub[["Jan", "Feb", "Mar", "Total"]].sum()
print(sum_row)
print("\n")

# Convert the values to columns and format it
df_sub_sum = pd.DataFrame(data=sum_row).T
df_sub_sum = df_sub_sum.applymap(money)
print(df_sub_sum)
print("\n")

# Add the total value to the DataFrame
final_table = formatted_df.append(df_sub_sum)
print(final_table)
print("\n")

# Changing the last index from '0' using rename()
final_table = final_table.rename(index={0: "Total"})
print(final_table)
