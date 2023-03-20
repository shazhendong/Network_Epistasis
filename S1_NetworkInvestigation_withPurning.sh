# This sh file performs network investigation for all networks in /data

#### Parameters ####
dir_input=data_purning
dir_output=res_purning
dir_script=scr

#### Main ####
# Create output directory
mkdir -p $dir_output

#### Investigate Mouse XOR ####
file_input=Mouse_XOR2W_filtered.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 2 -step 0.01 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -6 -th_h -2 -step 0.01 -mod se

#### Investigate Mouse Cart ####
file_input=Mouse_Cart2W_filtered.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 2 -step 0.01 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -6 -th_h -2 -step 0.01 -mod se

#### Investigate Rat XOR ####
file_input=Rat_XOR2W_filtered.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.01 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -8 -th_h -3 -step 0.01 -mod se

#### Investigate Rat Cart ####
file_input=Rat_Cart2W_filtered.csv
# investigate p-value from 0 to 0.05 step 0.00001 mode se
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_pval.csv -s snp1_name -t snp2_name -w adj_pval -th_l 0 -th_h 0.05 -step 0.0001 -mod se
# investigate ttest (positive)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_positive.csv -s snp1_name -t snp2_name -w ttest -th_l 4 -step 0.01 -mod ge
# investigate ttest (negative)
python $dir_script/networkInvestigation.py -i $dir_input/$file_input -o $dir_output/"$file_input"_networkInvestigation_ttest_negative.csv -s snp1_name -t snp2_name -w ttest -th_l -8 -th_h -3 -step 0.01 -mod se
