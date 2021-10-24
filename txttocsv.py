""" Data Cleaning file for Gingin Weather data received on March 11 2021.
    Data to be used for localised precipitation forecasting.
    Author: Matvey Solovyov Honours Student UWA OzGrav.
"""

import csv
import pandas as pd

from io import StringIO

# Data received in sql INSERT command, rows copied into text file
filename = "Mar11data.txt"

f = open(filename)
file = f.read()

# Each record was bound by parentheses, so these are removed
file = file.replace(")","").replace("(","")
# Each column name was in inverted commas, these are also removed
file = file.replace("'", "")

file = StringIO(file)

# String read in as csv
df = pd.read_csv(file, sep = ',', index_col = False)

# Removing whitespace from column names
df.columns = [col.strip() for col in df.columns]

# Saving dataframe as csv to be used elsewhere
df.to_csv('cleaned.csv',index=False)

# position 579808 has another insert statement, removed manually
