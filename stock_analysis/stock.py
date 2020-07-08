import numpy as np
import csv as csv
import pandas as pd
readdata = csv.reader(open("stock.csv"))
data = []

for row in readdata:
    data.append(row)

Header = data[0]
data.pop(0)
df = pd.DataFrame(data, columns=Header)
df.dropna(
    axis=0,
    how='any',
    inplace=True
)

def filter(df):
    df = df[df.PEG != 'N/A']
    df = df[df.PE != '']
    df = df[df.PE != 'NE']
    df = df[df['FORWARD PE'] != '']
    df = df[df['FORWARD PE'] != 'NE']
    df = df[df['EPS'] != '']
    df = df[df['EPS'] != 'NE']
    df = df[df['PEG'] != '']
    df = df[df['PEG'] != 'NE']
    df = df[df['EPS ESTIMATE'] != '']
    df = df[df['EPS ESTIMATE'] != 'NE']
    df = df[df['RECOMMENDATION'] != '']
    df = df[df['RECOMMENDATION'] != 'NE']
    types_dict = {
        'CURRENT PRICE': float,
        'PE': float,
        'FORWARD PE': float,
        'EPS': float,
        'PEG': float,
        'EPS ESTIMATE': float,
        'RECOMMENDATION': float
    }
    for col, col_type in types_dict.items():
        df[col] = df[col].astype(col_type)
    return df
df = filter(df)
# print(df)
# csv file has been read and cleaned

# current price
# industry
# pe
# forward pe
# eps estimate
# eps
# peg
# recommendation

# Filter by these industries
industries = [
    'Miscellaneous',
    'Finance',
    'Transportation',
    'Consumer%2bServices',
    'Capital%2bGoods',
    'Public%2bUtilities',
    'Basic%2bIndustries',
    'Health%2bCare',
    'Consumer%2bDurables',
    'Energy',
    'Technology',
    'Consumer%2bNon-Durables',
]
df = df[df['INDUSTRY'].isin(industries)]
#print(df) # print after filter

# Filter PEG
high_peg = 1.15 # max PEG value
low_peg = .05 # min PEG value
# low_peg <= PEG VALUE <= high_peg
df = df[(df['PEG'] >= low_peg) & (df['PEG'] <= high_peg)]

# Filter Low PE and FORWARD PE
# 10-17 is balanced (avg)
# 17-25 is good (good forcast)
# 25+ is bubble - potentially too high

# Filter out PE (and forward PE) >= 10
df = df[(df['PE'] >= 10) & (df['FORWARD PE'] >= 10)]
# Filter out unreasonable PE values (> 100)
df = df[(df['PE'] < 100) & (df['FORWARD PE'] < 100)]

# Filter EPS and EPS estimate

# ---------------------------

# Do calculation of EPS ESTIMATE * FORWARD PE
df = df[
    ((((df['EPS ESTIMATE'] * df['FORWARD PE'] - df['CURRENT PRICE'])
            / df['CURRENT PRICE'])
    > .35) & (df['PE'] * df['EPS ESTIMATE'] > df['CURRENT PRICE']))
    # |
    # (df['EPS'] * 2 < df['EPS ESTIMATE'])
]


# print(df)
df.to_csv('stock_selection.csv', index=False)




