# Author: Zhendong Sha@2022-02-08
# This program is used to investigate the network of a given graph (edge list).
# List of network characteristics to be investigated:
#   - Number of nodes
#   - Number of edges
#   - Number of connected components
#   - Size of the largest connected component
#   - Number of triangles

# Parameters:
#   -i: path to the input edge list file with header (csv) REQUIRED
#   -o: output file (csv) (default: networkInvestigation_output.csv)
#   -s: source node column name (default: source)
#   -t: to node column name (default: to)
#   -w: weight column name (default: weight)
#   -th_l: cut-off threshold begin ({max, min, #} default: min) 
#   -th_h: cut-off threshold end ({max, min, #} default: max)
#   -step: cut-off threshold step (default: 0.001)
#   -mod: the filtering mode ({se, s, ge, g} stands for {smaller or equal to, smaller, greater or equal to, greater} default: se)

# Example:
# python networkInvestigation.py -i fdr_var_significant_pairs_Cart.csv -s snp1_name -t snp2_name -w ttest -mod se -th_h 0 -step 0.1
# python networkInvestigation.py -i fdr_var_significant_pairs_Cart.csv -s snp1_name -t snp2_name -w ttest -mod ge -th_l 0 -step 0.1

import networkx as nx
import pandas as pd
import numpy as np
import multiprocessing as mp

# prepare edge list from input file
def prepare_edge_list(df, from_col, to_col, weight_col):
    # create edge list df using from_col, to_col, and weight_col columns
    df_edgelist = df[[from_col, to_col, weight_col]]
    # rename columns
    df_edgelist.columns = ["from", "to", "weight"]
    return df_edgelist

# setup thresholds
def setup_thresholds(threshold_begin, threshold_end, threshold_step, df_edgelist):
    # if threshold_begin is "max", set threshold_begin to the maximum weight in the edge list
    if threshold_begin == "max":
        threshold_begin = df_edgelist["weight"].max()
    # if threshold_begin is "min", set threshold_begin to the maximum weight in the edge list
    if threshold_begin == "min":
        threshold_begin = df_edgelist["weight"].min()
    # if threshold_end is "min", set threshold_end to the minimum weight in the edge list
    if threshold_end == "min":
        threshold_end = df_edgelist["weight"].min()
    # if threshold_end is "max", set threshold_end to the minimum weight in the edge list
    if threshold_end == "max":
        threshold_end = df_edgelist["weight"].max()

    # convert threshold_begin, threshold_end, and threshold_step to float
    threshold_begin = float(threshold_begin)
    threshold_end = float(threshold_end)
    threshold_step = float(threshold_step)
    return threshold_begin, threshold_end, threshold_step

# investigate a network
def investigate_network(df_edgelist, threshold, flt_mod, step):
    print("Investigating threshold " + str(threshold) + " ...")
    # filter edge list by threshold
    if flt_mod == "ge": # stand for greater than or equal to
        df_edgelist_T = df_edgelist[df_edgelist["weight"] >= threshold]
    elif flt_mod == "g": # stand for greater than
        df_edgelist_T = df_edgelist[df_edgelist["weight"] > threshold]
    elif flt_mod == "se": # stand for less than or equal to
        df_edgelist_T = df_edgelist[df_edgelist["weight"] <= threshold]
    elif flt_mod == "s": # stand for less than
        df_edgelist_T = df_edgelist[df_edgelist["weight"] < threshold]
    else:
        print("Error: invalid filtering mode")
        return None
    # create graph using edge list
    if df_edgelist_T.empty:
        print("Threshold " + str(threshold) + " has no edges. Skip.")
        return None
    
    # create undirected graph using edge list based on networkx
    g = nx.from_pandas_edgelist(df_edgelist_T, source="from", target="to", edge_attr="weight", create_using=nx.Graph())

    # calculate number of nodes
    num_nodes = g.number_of_nodes()

    # calculate number of edges
    num_edges = g.number_of_edges()
    
    # calculate number of connected components
    num_components = nx.number_connected_components(g)
    
    # calculate size of the largest connected component
    size_largest_component = max([len(c) for c in sorted(nx.connected_components(g), key=len, reverse=True)])
    
    # calculate number of triangles
    num_triangles = nx.triangles(g)
    num_triangles = sum(num_triangles.values()) / 3

    # calculate network modularity based on greedy modularity optimization
    modularity_greedy = nx.algorithms.community.modularity(g, nx.algorithms.community.greedy_modularity_communities(g))

    # calculate network modularity based on Louvain method
    # modularity_louvain = nx.algorithms.community.modularity(g, nx.algorithms.community.louvain_communities(g))

    # calculate clustering coefficient
    #clustering_coefficient = nx.clustering(g)
    
    # insert a row to output df using dict format
    # make a dict
    d = {"threshold": threshold, "num_nodes": num_nodes, "num_edges": num_edges, "num_components": num_components, "size_largest_component": size_largest_component, "num_triangles": num_triangles, "modularity_greedy": modularity_greedy}
    # prepare dataframe from d
    print(d)
    return pd.DataFrame(d, index=[0])

# investigate by a given threshold
def investigate_by_a_threshold(df_input, from_col, to_col, weight_col, threshold_begin, threshold_end, threshold_step, flt_mod):
    # prepare edge list
    df_edgelist = prepare_edge_list(df_input, from_col, to_col, weight_col)
    # initialize output df
    # df_output = pd.DataFrame(columns=["threshold", "num_nodes", "num_edges", "num_components", "size_largest_component", "num_triangles"])
    df_output = pd.DataFrame()
    # setup thresholds
    threshold_begin, threshold_end, threshold_step = setup_thresholds(threshold_begin, threshold_end, threshold_step, df_edgelist)
    print("threshold_begin: " + str(threshold_begin) + ", threshold_end: " + str(threshold_end) + ", threshold_step: " + str(threshold_step))
    # perform network investigation using multiprocessing
    # create a pool of processes
    pool = mp.Pool(mp.cpu_count())
    # prepare arguments
    args = [(df_edgelist, threshold, flt_mod, threshold_step) for threshold in np.arange(threshold_begin, threshold_end+threshold_step, threshold_step)]
    # start multiprocessing
    results = pool.starmap(investigate_network, args)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
    # concatenate results
    for result in results:
        if result is not None:
            df_output = pd.concat([df_output, result], axis=0)
    return df_output

# investigate by two thresholds
def investigate_by_two_thresholds(df_input, from_col, to_col, weight_col, threshold_begin, threshold_end, threshold_step, flt_mod, weight_col2, threshold_begin2, threshold_end2, threshold_step2, flt_mod2):
    # prepare edge list
    df_edgelist = prepare_edge_list(df_input, from_col, to_col, weight_col)
    # initialize output df
    df_output = pd.DataFrame()
    # setup thresholds
    threshold_begin, threshold_end, threshold_step = setup_thresholds(threshold_begin, threshold_end, threshold_step, df_edgelist)
    print("threshold_begin: " + str(threshold_begin) + ", threshold_end: " + str(threshold_end) + ", threshold_step: " + str(threshold_step))
    # loop through thresholds
    for threshold in np.arange(threshold_begin, threshold_end+threshold_step, threshold_step):
        print("threshold: " + str(threshold))
        # filter input by threshold
        if flt_mod == "ge": # stand for greater than or equal to
            # select rows where weight_col >= threshold
            input_T = df_input[df_input[weight_col] >= threshold]
        elif flt_mod == "g": # stand for greater than
            input_T = df_input[df_input[weight_col] > threshold]
        elif flt_mod == "se": # stand for less than or equal to
            input_T = df_input[df_input[weight_col] <= threshold]
        elif flt_mod == "s": # stand for less than
            input_T = df_input[df_input[weight_col] < threshold]
        else:
            print("Error: invalid filtering mode for mod1")
            break
        # continue to filter input_T is empty
        if input_T.empty:
            print("Threshold " + str(threshold) + " has no edges. Skip.")
            continue
        df_t=investigate_by_a_threshold(input_T, from_col, to_col, weight_col2, threshold_begin2, threshold_end2, threshold_step2, flt_mod2)
        # update threshold column name with weight_col2
        df_t.rename(columns={"threshold": "threshold_"+str(weight_col2)}, inplace=True)
        # add threshold column to df_t
        df_t["threshold"] = threshold
        # move threshold column to the first column
        cols = df_t.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_t = df_t[cols]
        # rename the threshold column to weight_col
        df_t.rename(columns={"threshold": "threshold_"+str(weight_col)}, inplace=True)
        # concat df to output df
        df_output = pd.concat([df_output, df_t], ignore_index=True)


    return df_output



# read parameters and call the main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input edge list file (csv)")
    parser.add_argument("-o", "--output", required=False, default="networkInvestigation_output.csv", help="output file (csv)")
    parser.add_argument("-s", "--source", default="source", help="source node column name (default: source)")
    parser.add_argument("-t", "--to", default="to", help="to node column name (default: to)")
    parser.add_argument("-w", "--weight", default="weight", help="weight column name (default: weight)")
    parser.add_argument("-th_l", "--threshold_lower", default="min", help="cut-off threshold lower limit (default: max)")
    parser.add_argument("-th_h", "--threshold_upper", default="max", help="cut-off threshold upper limit (default: min)")
    parser.add_argument("-step", "--threshold_step", default=0.001, help="cut-off threshold step (default: 0.001)")
    parser.add_argument("-mod", "--filter_mode", default="se", help="the filtering mode (default: se)")
    parser.add_argument("-w2", "--weight2", default=None, help="weight column name (default: weight)")
    parser.add_argument("-th_l2", "--threshold_lower2", default="min", help="cut-off threshold lower limit (default: max)")
    parser.add_argument("-th_h2", "--threshold_upper2", default="max", help="cut-off threshold upper limit (default: min)")
    parser.add_argument("-step2", "--threshold_step2", default=0.001, help="cut-off threshold step (default: 0.001)")
    parser.add_argument("-mod2", "--filter_mode2", default="se", help="the filtering mode (default: se)")
    args = parser.parse_args()
    
    # read input file
    df_input = pd.read_csv(args.input)

    # if w2 is not None, then perform network investigation for two thresholds
    if args.weight2 is not None:
        print("investigate by two thresholds")
        df_out = investigate_by_two_thresholds(df_input, args.source, args.to, args.weight, args.threshold_lower, args.threshold_upper, args.threshold_step, args.filter_mode, args.weight2, args.threshold_lower2, args.threshold_upper2, args.threshold_step2, args.filter_mode2)
    else:
        print("investigate by one threshold")
        df_out = investigate_by_a_threshold(df_input, args.source, args.to, args.weight, args.threshold_lower, args.threshold_upper, args.threshold_step, args.filter_mode)
    df_out.to_csv(args.output, index=False)
