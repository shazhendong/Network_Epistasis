# This python script is used to compare the edgelists of two graphs.
# It takes two edgelists as input and outputs the common edges and the edges that are in one graph but not the other.
# Each node in the edge list is in the format of "chr+chr#_pos#_refallele" (e.g. chr7.92716677_G)
# This comparision do not require edges to be exactly the same. It allows a range of difference in the chr pos of the edges.
# The edgelist should be in the format of "from,to,weight"
# Parameters: edgelist1, edgelist2, range
# Output: edgelist1_common_range.csv, edgelist1_only_range.csv, edgelist2_common_range.csv, edgelist2_only_range.csv


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

# function to determine if two edges are the same
# return true if they are the same, false if not
def compare(edge1_node_from_name, edge1_node_to_name, edge2_node_from_name, edge2_node_to_name, range):\
    # delete chr from the node name
    edge1_node_from_name = edge1_node_from_name[3:]
    edge1_node_to_name = edge1_node_to_name[3:]
    edge2_node_from_name = edge2_node_from_name[3:]
    edge2_node_to_name = edge2_node_to_name[3:]

    # delete the ref allele from the node name.
    edge1_node_from_name = edge1_node_from_name.split("_")[0]
    edge1_node_to_name = edge1_node_to_name.split("_")[0]
    edge2_node_from_name = edge2_node_from_name.split("_")[0]
    edge2_node_to_name = edge2_node_to_name.split("_")[0]

    # get the chr and pos from the node name.
    edge1_node_from_chr = edge1_node_from_name.split(".")[0]
    edge1_node_from_pos = edge1_node_from_name.split(".")[1]
    edge1_node_to_chr = edge1_node_to_name.split(".")[0]
    edge1_node_to_pos = edge1_node_to_name.split(".")[1]
    edge2_node_from_chr = edge2_node_from_name.split(".")[0]
    edge2_node_from_pos = edge2_node_from_name.split(".")[1]
    edge2_node_to_chr = edge2_node_to_name.split(".")[0]
    edge2_node_to_pos = edge2_node_to_name.split(".")[1]

    # convert the chr and pos to int
    edge1_node_from_chr = int(edge1_node_from_chr)
    edge1_node_from_pos = int(edge1_node_from_pos)
    edge1_node_to_chr = int(edge1_node_to_chr)
    edge1_node_to_pos = int(edge1_node_to_pos)
    edge2_node_from_chr = int(edge2_node_from_chr)
    edge2_node_from_pos = int(edge2_node_from_pos)
    edge2_node_to_chr = int(edge2_node_to_chr)
    edge2_node_to_pos = int(edge2_node_to_pos)

    # compare edge1_from with edge2_from and edge1_to with edge2_to
    if edge1_node_from_chr == edge2_node_from_chr and edge1_node_to_chr == edge2_node_to_chr:
        if abs(edge1_node_from_pos - edge2_node_from_pos) <= range and abs(edge1_node_to_pos - edge2_node_to_pos) <= range:
            print("COMMON", "edge1_from: ", edge1_node_from_name, "edge2_from: ", edge2_node_from_name, "edge1_to: ", edge1_node_to_name, "edge2_to: ", edge2_node_to_name)
            return True
    
    # compare edge1_from with edge2_to and edge1_to with edge2_from
    if edge1_node_from_chr == edge2_node_to_chr and edge1_node_to_chr == edge2_node_from_chr:
        if abs(edge1_node_from_pos - edge2_node_to_pos) <= range and abs(edge1_node_to_pos - edge2_node_from_pos) <= range:
            print("COMMON", "edge1_from: ", edge1_node_from_name, "edge2_to: ", edge2_node_to_name, "edge1_to: ", edge1_node_to_name, "edge2_from: ", edge2_node_from_name)
            return True
    
    # print("NOT COMMON", "edge1_from: ", edge1_node_from_name, "edge2_from: ", edge2_node_from_name, "edge1_to: ", edge1_node_to_name, "edge2_to: ", edge2_node_to_name)
    return False

# initialize the G1 common edges list
G1_common_edges = []
# initialize the G1 only edges list
G1_only_edges = []
# initialize the G2 common edges list
G2_common_edges = []
# initialize the G2 only edges list
G2_only_edges = []

# loop through the edges in G1
for edge1 in G1.edges():
    # get the node names of edge1
    edge1_node_from_name = edge1[0]
    edge1_node_to_name = edge1[1]
    # loop through the edges in G2
    for edge2 in G2.edges():
        # get the node names of edge2
        edge2_node_from_name = edge2[0]
        edge2_node_to_name = edge2[1]
        # compare edge1 and edge2
        if compare(edge1_node_from_name, edge1_node_to_name, edge2_node_from_name, edge2_node_to_name, range):
            # add edge1 to common edges
            G1_common_edges.append((edge1_node_from_name, edge1_node_to_name))
            break
# prepare the G1 only edges list
for edge1 in G1.edges():
    # get the node names of edge1
    edge1_node_from_name = edge1[0]
    edge1_node_to_name = edge1[1]
    # if edge1 is not in G1_common_edges, add it to G1_only_edges
    if (edge1_node_from_name, edge1_node_to_name) not in G1_common_edges:
        G1_only_edges.append((edge1_node_from_name, edge1_node_to_name))

# loop through the edges in G2
for edge2 in G2.edges():
    # get the node names of edge2
    edge2_node_from_name = edge2[0]
    edge2_node_to_name = edge2[1]
    # loop through the edges in G1
    for edge1 in G1.edges():
        # get the node names of edge1
        edge1_node_from_name = edge1[0]
        edge1_node_to_name = edge1[1]
        # compare edge1 and edge2
        if compare(edge1_node_from_name, edge1_node_to_name, edge2_node_from_name, edge2_node_to_name, range):
            # add edge2 to common edges
            G2_common_edges.append((edge2_node_from_name, edge2_node_to_name))
            break
# prepare the G2 only edges list
for edge2 in G2.edges():
    # get the node names of edge2
    edge2_node_from_name = edge2[0]
    edge2_node_to_name = edge2[1]
    # if edge2 is not in G2_common_edges, add it to G2_only_edges
    if (edge2_node_from_name, edge2_node_to_name) not in G2_common_edges:
        G2_only_edges.append((edge2_node_from_name, edge2_node_to_name))

# print the number of edges in each category
print("Number of common edges in G1: ", len(G1_common_edges))
print("Number of edges in G1 but not in G2: ", len(G1_only_edges))
print("Number of common edges in G2: ", len(G2_common_edges))
print("Number of edges in G2 but not in G1: ", len(G2_only_edges))

# prepare the df for each category. with the format of "from,to"
df_G1_common_edges = pd.DataFrame(G1_common_edges, columns=['from', 'to'])
df_G1_only_edges = pd.DataFrame(G1_only_edges, columns=['from', 'to'])
df_G2_common_edges = pd.DataFrame(G2_common_edges, columns=['from', 'to'])
df_G2_only_edges = pd.DataFrame(G2_only_edges, columns=['from', 'to'])

# save the df to csv
df_G1_common_edges.to_csv(sys.argv[1] + "_common_range.csv", index=False)
df_G1_only_edges.to_csv(sys.argv[1] + "_only_range.csv", index=False)
df_G2_common_edges.to_csv(sys.argv[2] + "_common_range.csv", index=False)
df_G2_only_edges.to_csv(sys.argv[2] + "_only_range.csv", index=False)
