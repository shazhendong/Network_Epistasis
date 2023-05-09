# This pipeline compare two edgelists and produce the common and specific edges.
# Author: Zhendong Sha 2023-05-09

# The edgelist should be in the format of "from,to,weight"

#### Parameters ####
dir_target=res_purning
dir_input=$dir_target/network_filterings
dir_output=$dir_input/compare_for_ratcart_ratxors

file_network1=Rat_XOR2W_filtered.csv.pvalue_cutoff_0.0434.mod_se.edgelist.csv
file_network1_community=Rat_XOR2W_filtered.csv.pvalue_cutoff_0.0434.mod_se.edgelist.csv.community.enrichment_range_1000000.csv
file_network2=Rat_Cart2W_filtered.csv.pvalue_cutoff_0.0488.mod_se.edgelist.csv
file_network2_community=Rat_Cart2W_filtered.csv.pvalue_cutoff_0.0488.mod_se.edgelist.csv.community.enrichment_range_1000000.csv

dir_script=scr
file_script_comp_net=edgelist_comparison.py
file_add_col=addColumn2df.py
file_scr_comp_comm=community_comparison.py

#### Main ####
# prepare the output folder
# rm -rf $dir_output
mkdir -p $dir_output

# compare the two edgelists
python $dir_script/$file_script_comp_net $dir_input/$file_network1 $dir_input/$file_network2
# rename the output files
# edgelist1_only.csv -> $file_network1.only.csv
mv edgelist1_only.csv $file_network1.only.csv
# edgelist2_only.csv -> $file_network2.only.csv
mv edgelist2_only.csv $file_network2.only.csv

# make cytoscpe ready edgelists
# add the column "type" to the edgelists
python $dir_script/$file_add_col $file_network1.only.csv type XOR
python $dir_script/$file_add_col $file_network2.only.csv type CART
python $dir_script/$file_add_col common_edges.csv type COMMON
# remove the header of the edgelists and saved as headerless files
tail -n +2 $file_network1.only.csv > $file_network1.only.csv.headerless
tail -n +2 $file_network2.only.csv > $file_network2.only.csv.headerless
# combine the edgelists
cat common_edges.csv $file_network1.only.csv.headerless $file_network2.only.csv.headerless > cytoscapeReady_combined_edgelist.csv

# compare the two community files
python $dir_script/$file_scr_comp_comm $dir_input/$file_network1_community $dir_input/$file_network2_community community node xor cart

# clean up
mv common_edges.csv $dir_output
mv $file_network1.only.csv $dir_output
mv $file_network2.only.csv $dir_output
mv cytoscapeReady_combined_edgelist.csv $dir_output
rm $file_network1.only.csv.headerless
rm $file_network2.only.csv.headerless

mv community_comparison.csv $dir_output