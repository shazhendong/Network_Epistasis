# This pipeline filter the network by threshold, produce the edgelist and determin the network community.
# Author: Zhendong Sha 2023-04-16

#### Parameters ####
dir_target=res_purning
dir_output=network_filterings
dir_input=data_purning
file_rat_cat=Rat_Cart2W_filtered.csv
file_rat_xor=Rat_XOR2W_filtered.csv
file_mouse_cat=Mouse_Cart2W_filtered.csv
file_mouse_xor=Mouse_XOR2W_filtered.csv

dir_script=scr
file_script_filter=edge_filter.py
file_script_community=network_community.py

# save pwd to home
home=$(pwd)

#### Main ####

cd $dir_target
mkdir -p $dir_output
cd $dir_output

## process rat_xor
edgelist=$file_rat_xor
cutoff_p=0.0434

# copy the edgelist to the output folder
cp $home/$dir_input/$edgelist .
# filter the edgelist by pvalue threshold
python $home/$dir_script/$file_script_filter $edgelist snp1_name snp2_name adj_pval $cutoff_p se edge_list.csv
# rename the edgelist
name_edgelist=$edgelist.pvalue_cutoff_$cutoff_p.mod_se.edgelist.csv
mv edge_list.csv $name_edgelist
# determin the network community
python $home/$dir_script/$file_script_community $name_edgelist community.csv
# rename the community file
name_community=$name_edgelist.community.csv
mv community.csv $name_community

# remove the edgelist
rm $edgelist