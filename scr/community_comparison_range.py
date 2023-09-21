# compare the communities of two graphs. two nodes are considered to be in the same if their positions are located within a range.
# Parameters: 
#   1. community1.csv 
#   2. community2.csv 
#   3. community column name
#   4. node name column name
#   5. alias of community1
#   6. alias of community2
#   7. range (int)
# Output: community_comparison_matrix.csv

import sys
import pandas as pd

# read the community files
df_community1 = pd.read_csv(sys.argv[1])
df_community2 = pd.read_csv(sys.argv[2])
# read the community column name
community_col_name = sys.argv[3]
# read the node name column name
node_name_col_name = sys.argv[4]
# get the alias of community1
community1_alias = sys.argv[5]
# get the alias of community2
community2_alias = sys.argv[6]
# get the range
snp_range = int(sys.argv[7])

# get subdfs for each community
df_community1_subdfs = []
community1_names = df_community1[community_col_name].unique()
df_community2_subdfs = []
community2_names = df_community2[community_col_name].unique()
# for each community name in community1
for community_name in community1_names:
    # get the subdf for this community
    df_community1_subdfs.append(df_community1[df_community1[community_col_name] == community_name])
# for each community name in community2
for community_name in community2_names:
    # get the subdf for this community
    df_community2_subdfs.append(df_community2[df_community2[community_col_name] == community_name])

# define a function to check if two nodes names are the same considering the range
def is_same_node_name(node_name1, node_name2, snp_range):
    # translate node name from name to chr and pos (chr3.10579003_A -> chr=3, pos=10579003)
    node_name1_chr = int(node_name1.split('.')[0].replace('chr', ''))
    node_name1_pos = int(node_name1.split('.')[1].split('_')[0])
    node_name2_chr = int(node_name2.split('.')[0].replace('chr', ''))
    node_name2_pos = int(node_name2.split('.')[1].split('_')[0])
    # check if the two nodes are on the same chromosome
    if node_name1_chr != node_name2_chr:
        return False
    # check if the two nodes are within the range
    if abs(node_name1_pos - node_name2_pos) <= snp_range:
        return True
    else:
        return False

# create the community comparison df with the format of "community1_alias,community2_alias,common_nodes_number"
df_community_comparison = pd.DataFrame(columns=[community1_alias, community2_alias, 'common_nodes_number'])
# for each community in community1 by index
for i in range(len(df_community1_subdfs)):
    # for each community in community2 by index
    for j in range(len(df_community2_subdfs)):
        # get the common nodes number (do not consider range)
        #common_nodes_number_norange = len(list(set(df_community1_subdfs[i][node_name_col_name]) & set(df_community2_subdfs[j][node_name_col_name])))
        # get the common nodes number (consider range)
        common_nodes_number_wihtrange = 0
        # for each node in community1
        for node_name1 in df_community1_subdfs[i][node_name_col_name]:
            # for each node in community2
            for node_name2 in df_community2_subdfs[j][node_name_col_name]:
                # check if the two nodes are the same
                if is_same_node_name(node_name1, node_name2, snp_range):
                    common_nodes_number_wihtrange += 1
                    break # each node in community1 can only be matched once
        # append the row to the community comparison df do not use append
        df_community_comparison.loc[len(df_community_comparison)] = [community1_names[i], community2_names[j],common_nodes_number_wihtrange]

# add the alias to community1 and community2 columns in df_community_comparison
df_community_comparison[community1_alias] = df_community_comparison[community1_alias].apply(lambda x: community1_alias + '_c_' + str(x))
df_community_comparison[community2_alias] = df_community_comparison[community2_alias].apply(lambda x: community2_alias + '_c_' + str(x))

# delete rows with common_nodes_number = 0
df_community_comparison = df_community_comparison[df_community_comparison['common_nodes_number'] != 0]

# sort the df by common_nodes_number
df_community_comparison = df_community_comparison.sort_values(by=['common_nodes_number'], ascending=False)

# save the community comparison df to csv
df_community_comparison.to_csv('community_comparison.csv', index=False)

