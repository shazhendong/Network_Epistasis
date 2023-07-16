# This pipeline perform analysis for tri-angles in the epistatic network. It first filter the network by threshold, produce the edgelist and perform analysis. 1) get triangles 2) get snp names 3) prepare for enrichment analysis.
# Author: Zhendong Sha 2023-07-16

#### Parameters ####
dir_target=res_purning
dir_output=triangles
dir_input=data_purning
file_rat_cat=Rat_Cart2W_filtered.csv
file_rat_xor=Rat_XOR2W_filtered.csv

dir_script=scr
file_script_filter=edge_filter.py
file_script_getTriangles=get_triangles_from_edgelist.py
file_script_community=network_community.py
file_prepare_snp=prepare_snp_for_gProfiler.py
snp_range=1000000

# save pwd to home
home=$(pwd)

#### Main ####

cd $dir_target
mkdir -p $dir_output
cd $dir_output

## process rat_xor
echo "Processing rat_xor"
edgelist=$file_rat_xor
cutoff_p=0.0434

# copy the edgelist to the output folder
cp $home/$dir_input/$edgelist .

## p-value filtering
echo "p-value filtering with cutoff $cutoff_p"
# filter the edgelist by pvalue threshold
python $home/$dir_script/$file_script_filter $edgelist snp1_name snp2_name adj_pval $cutoff_p se edge_list.csv
# rename the edgelist
name_edgelist=$edgelist.pvalue_cutoff_$cutoff_p.mod_se.edgelist.csv # edge list file name
mv edge_list.csv $name_edgelist
# get triangles
python $home/$dir_script/$file_script_getTriangles -i $name_edgelist -o1 triangles.csv -o2 triangles_snp.csv
# rename the triangles file
name_triangles=$name_edgelist.triangles.csv
mv triangles.csv $name_triangles
# rename the triangles_snp file
name_triangles_snp=$name_edgelist.triangles_snp.csv
mv triangles_snp.csv $name_triangles_snp
# prepare the snp coordinates for gProfiler
python $home/$dir_script/$file_prepare_snp -i $name_triangles_snp -o $name_triangles_snp -r $snp_range -c snp

# remove the edgelist
rm $edgelist

## process rat_cart
echo "Processing rat_cart"
edgelist=$file_rat_cat
cutoff_p=0.0488

# copy the edgelist to the output folder
cp $home/$dir_input/$edgelist .

## p-value filtering
echo "p-value filtering with cutoff $cutoff_p"
# filter the edgelist by pvalue threshold
python $home/$dir_script/$file_script_filter $edgelist snp1_name snp2_name adj_pval $cutoff_p se edge_list.csv
# rename the edgelist
name_edgelist=$edgelist.pvalue_cutoff_$cutoff_p.mod_se.edgelist.csv # edge list file name
mv edge_list.csv $name_edgelist
# get triangles
python $home/$dir_script/$file_script_getTriangles -i $name_edgelist -o1 triangles.csv -o2 triangles_snp.csv
# rename the triangles file
name_triangles=$name_edgelist.triangles.csv
mv triangles.csv $name_triangles
# rename the triangles_snp file
name_triangles_snp=$name_edgelist.triangles_snp.csv
mv triangles_snp.csv $name_triangles_snp
# prepare the snp coordinates for gProfiler
python $home/$dir_script/$file_prepare_snp -i $name_triangles_snp -o $name_triangles_snp -r $snp_range -c snp

# remove the edgelist
rm $edgelist
