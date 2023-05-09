# This python add a column of same value to a dataframe.
# Parameters: 
# 1. df: the dataframe to be added a column
# 2. col_name: the name of the column to be added
# 3. col_value: the value of the column to be added


import pandas as pd
import sys

# read the dataframe
df = pd.read_csv(sys.argv[1])

# read the column name
col_name = sys.argv[2]

# read the column value
col_value = sys.argv[3]

# add the column
df[col_name] = col_value

# save the dataframe
df.to_csv(sys.argv[1], index=False)