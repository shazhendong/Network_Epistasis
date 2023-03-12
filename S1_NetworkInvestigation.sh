# This sh file performs network investigation for all networks in /data

#### Parameters ####
dir_input=data
dir_output=res_comp
dir_script=scr

#### Main ####
# Create output directory
mkdir -p $dir_output

#### Investigate significant_xor_mouse.csv ####
file_input=significant_xor_mouse.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.1 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -10 -step 0.1 -mod se

#### Investigate significant_cart_mouse.csv ####
file_input=significant_cart_mouse.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.1 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -10 -step 0.1 -mod se

#### Investigate xor_significant_rat.csv ####
file_input=xor_significant_rat.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.1 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -10 -step 0.1 -mod se

#### cartesian_significant_rat.csv ####
file_input=cartesian_significant_rat.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.1 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -10 -step 0.1 -mod se
