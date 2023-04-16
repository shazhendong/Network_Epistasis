# this python script is used to filter the edgelist
# Parameters:
#   1. edgelist file
#   2. source node column name
#   3. target node column name
#   4. weight: the name of the edge weight
#   5. cutoff: the cutoff value of the edge weight
#   6. mode: 'se' stands for smaller or equal to cutoff, 'ge' stands for greater or equal to cutoff
#   7. output file

import sys

# read all parameters
edgelist_file = sys.argv[1] # the edgelist file
source = sys.argv[2] # source node column name
target = sys.argv[3] # target node column name
weight = sys.argv[4] # the name of the edge weight
cutoff = float(sys.argv[5]) # the cutoff value of the edge weight
mode = sys.argv[6] # 'se' stands for smaller or equal to cutoff, 'ge' stands for greater or equal to cutoff
output_file = sys.argv[7] # the output file

# read the edgelist file
import pandas as pd
df_edges = pd.read_csv(edgelist_file, sep=',') # read the edgelist file

# filter the edgelist
if mode == 'se':
    # print('mode is se')
    df_edges = df_edges[df_edges[weight] <= cutoff]
elif mode == 'ge':
    # print('mode is ge')
    df_edges = df_edges[df_edges[weight] >= cutoff]
else:
    print('mode should be se or ge')

# get the source and target nodes and the edge weights
source_nodes = df_edges[source].tolist()
target_nodes = df_edges[target].tolist()
edge_weights = df_edges[weight].tolist()

# prepare the output df
df_output = pd.DataFrame()
df_output['from'] = source_nodes
df_output['to'] = target_nodes
df_output['weight'] = edge_weights

# write the output file
df_output.to_csv(output_file, sep=',', index=False)
