# this python file determin the community of each node
# Parameters:
#   1. edgelist file (header: from, to, weight)
#   2. output file (header: node, community)

# read edge list from file
import pandas as pd
import networkx as nx

# read edgelist from file
import sys
df_edgelist = pd.read_csv(sys.argv[1], sep=',')
# prepare the nx graph from the df_edgelist
g = nx.from_pandas_edgelist(df_edgelist, 'from', 'to', 'weight')

# identify the communities using greedy community detection
community=nx.algorithms.community.greedy_modularity_communities(g)

# iterate through the communities
df_community = pd.DataFrame()
for i, c in enumerate(community):
    # make df for each community
    df_community_t = pd.DataFrame()
    df_community_t['node'] = list(c)
    df_community_t['community'] = i
    # concatenate the df
    df_community = pd.concat([df_community, df_community_t], axis=0)

# write the community to file
df_community.to_csv(sys.argv[2], sep=',', index=False)
