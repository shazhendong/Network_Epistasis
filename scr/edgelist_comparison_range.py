# This python script is used to compare the edgelists of two graphs.
# It takes two edgelists as input and outputs the common edges and the edges that are in one graph but not the other.
# The edgelist should be in the format of "from,to,weight"
# Parameters: edgelist1, edgelist2, range
# Output: common_edges_"range".csv, edgelist1_only_"range".csv, edgelist2_only_"range".csv


import sys
import csv
import os
import pandas as pd
import networkx as nx

# Read the edgelists
df_edgelist1 = pd.read_csv(sys.argv[1])
df_edgelist2 = pd.read_csv(sys.argv[2])

# read the range
range = int(sys.argv[3])

# Prepare undirected nx networks from the edgelists df
G1 = nx.from_pandas_edgelist(df_edgelist1, source='from', target='to', edge_attr='weight', create_using=nx.Graph())
G2 = nx.from_pandas_edgelist(df_edgelist2, source='from', target='to', edge_attr='weight', create_using=nx.Graph())

# Get the common edges
common_edges = list(set(G1.edges()) & set(G2.edges()))

# Get the edges that are in G1 but not in G2
G1_only_edges = list(set(G1.edges()) - set(G2.edges()))

# Get the edges that are in G2 but not in G1
G2_only_edges = list(set(G2.edges()) - set(G1.edges()))

# print the number of edges in each category
print("Number of common edges: ", len(common_edges))
print("Number of edges in G1 but not in G2: ", len(G1_only_edges))
print("Number of edges in G2 but not in G1: ", len(G2_only_edges))

# prepare the df for each category. with the format of "from,to"
df_common_edges = pd.DataFrame(common_edges, columns=['from', 'to'])
df_G1_only_edges = pd.DataFrame(G1_only_edges, columns=['from', 'to'])
df_G2_only_edges = pd.DataFrame(G2_only_edges, columns=['from', 'to'])

# save the df to csv
df_common_edges.to_csv("common_edges_" + str(range) + ".csv", index=False)
df_G1_only_edges.to_csv("edgelist1_only_" + str(range) + ".csv", index=False)
df_G2_only_edges.to_csv("edgelist2_only_" + str(range) + ".csv", index=False)