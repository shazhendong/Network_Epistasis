# get the community metadata.
# Parameters: 
#   1. community.csv 
#   2. community column name
#   3. node name column name
# Output: community_metadata.csv

import sys
import pandas as pd

# read the community files
df_community1 = pd.read_csv(sys.argv[1])
# read the community column name
community_col_name = sys.argv[2]
# read the node name column name
node_name_col_name = sys.argv[3]

# get subdfs for each community
df_community1_subdfs = []
community1_names = df_community1[community_col_name].unique()

# for each community name in community1
for community_name in community1_names:
    # get the subdf for this community
    df_community1_subdfs.append(df_community1[df_community1[community_col_name] == community_name])

# create the community metadata df with the format of "community_name,community_size"
df_community_metadata = pd.DataFrame(columns=['community_name', 'community_size'])

# for each community in community1 by index
for i in range(len(df_community1_subdfs)):
    # get the community size
    community_size = len(df_community1_subdfs[i])
    # append the row to the community metadata df do not use append
    df_community_metadata.loc[len(df_community_metadata)] = [community1_names[i], community_size]

# sort the df by community_size
df_community_metadata = df_community_metadata.sort_values(by=['community_size'], ascending=False)

# save the community metadata df to csv
df_community_metadata.to_csv('community_metadata.csv', index=False)

