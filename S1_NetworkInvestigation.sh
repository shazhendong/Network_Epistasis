# This sh file performs network investigation for all networks in /data

#### Parameters ####
dir_input=data
dir_output=res
dir_script=scr

#### Main ####
# Create output directory
mkdir -p $dir_output

#### Investigate significant_xor_mouse.csv ####
file_input=significant_xor_mouse.csv
# get fine name of input file
file_input_name=$(basename $file_input)
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input_name"_networkInvestigation_pval_f1.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.0001 -step 0.00001 -mod se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input_name"_networkInvestigation_pval_f2.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0.01 -th_h 0.011 -step 0.0001 -mod se
# exclude the first line of the f2 file
tail -n +2 $dir_output/"$file_input_name"_networkInvestigation_pval_f2.csv > $dir_output/"$file_input_name"_networkInvestigation_pval_f2_excl.csv
# concatenate the two files
cat $dir_output/"$file_input_name"_networkInvestigation_pval_f1.csv $dir_output/"$file_input_name"_networkInvestigation_pval_f2_excl.csv > $dir_output/"$file_input_name"_networkInvestigation_pval.csv
# remove intermediate files
rm $dir_output/"$file_input_name"_networkInvestigation_pval_f1.csv
rm $dir_output/"$file_input_name"_networkInvestigation_pval_f2.csv
rm $dir_output/"$file_input_name"_networkInvestigation_pval_f2_excl.csv

#### Investigate significant_cart_mouse.csv ####

#### Investigate xor_significant_rat.csv ####

#### cartesian_significant_rat.csv ####
