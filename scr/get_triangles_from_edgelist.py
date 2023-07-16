# this python file get the triangles from a edge list file.
# Parameters:
# -i: input file
# -o1: output file_triangles
# -o2: output file_snp_list

import argparse
import pandas as pd
from itertools import combinations

# read parameters
parser = argparse.ArgumentParser(description='Get triangles from edgelist')
parser.add_argument('-i', '--input', help='Input file', required=True)
parser.add_argument('-o1', '--output1', help='Output file_triangles', required=True)
parser.add_argument('-o2', '--output2', help='Output file_snp_list', required=True)

args = parser.parse_args()

# read input edge list file
df = pd.read_csv(args.input, sep=',')

# convert edgelist to networkx graph
import networkx as nx
G = nx.from_pandas_edgelist(df, 'from', 'to', ['weight'])

# Get all the triangles from the graph
triangles = set()
for node in G.nodes():
    neighbors = set(G.neighbors(node))
    for pair in combinations(neighbors, 2):
        if G.has_edge(pair[0], pair[1]):
            triangle = tuple(sorted([node, pair[0], pair[1]]))
            triangles.add(triangle)

# Convert the set of triangles back to a list
triangles = list(triangles)

# convert tranigles to dataframe
df_triangles = pd.DataFrame(triangles, columns=['snp1', 'snp2', 'snp3'])

# convert triangles to snp list (unique snps)
snp_list = list(set(df_triangles['snp1'].tolist() + df_triangles['snp2'].tolist() + df_triangles['snp3'].tolist()))

# convert snp list to dataframe
df_snp_list = pd.DataFrame(snp_list, columns=['snp'])

# write output files
df_triangles.to_csv(args.output1, sep=',', index=False)
df_snp_list.to_csv(args.output2, sep=',', index=False)