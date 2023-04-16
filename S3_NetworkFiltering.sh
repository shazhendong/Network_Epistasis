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
file_script=edge_filter.py

# save pwd to home
home=$(pwd)

#### Main ####

cd $dir_target
mkdir -p $dir_output
cd $dir_output

## process rat_xor
edgelist=$file_rat_xor
cutoff_p=0.03

# copy the edgelist to the output folder
cp $home/$dir_input/$edgelist .
# filter the edgelist by pvalue threshold
python $home/$dir_script/$file_script $edgelist snp1_name snp2_name adj_pval 0.03 se edge_list.csv
# rename the edgelist
mv edge_list.csv $edgelist.pvalue_cutoff_$cutoff_p.mod_se.csv
# determin the network community
python $home/$dir_script/$file_script $edgelist.pvalue_cutoff_$cutoff_p.mod_se.csv snp1_name snp2_name adj_pval 0.03 se edge_list.csv

# remove the edgelist
rm $edgelist