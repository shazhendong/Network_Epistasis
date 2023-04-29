# This pipeline determines the partical optimal point of the network filtering process based on p-value.
# Author: Zhendong Sha 2023-04-28

#### Parameters ####
dir_target=res_purning
dir_output=inflection_point

dir_script=scr
file_script=identify_partial_optimalCutoff.py

sensitivity_begin=0.9
sensitivity_end=1.0
sensitivity_step=0.01

# save pwd to home
home=$(pwd)

#### Main ####

# for each file in the target folder

cd $dir_target
# rm -rf $dir_output
mkdir -p $dir_output

# investigate the rat xor
echo "investigate the rat xor"
data=Rat_XOR2W_filtered.csv_networkInvestigation_pval.csv
file_output=partialOpt_rat_xor.csv

rm $dir_output/$file_output

touch $dir_output/$file_output
echo "x, partial_y, fraction" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -f $sensitivity >> $dir_output/$file_output
done


# investigate the rat cart
echo "investigate the rat cart"
data=Rat_Cart2W_filtered.csv_networkInvestigation_pval.csv
file_output=partialOpt_rat_cart.csv

rm $dir_output/$file_output

touch $dir_output/$file_output
echo "x, partial_y, fraction" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python3 $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -f $sensitivity >> $dir_output/$file_output
done

# investigate the mouse xor
echo "investigate the mouse xor"
data=Mouse_XOR2W_filtered.csv_networkInvestigation_pval.csv
file_output=partialOpt_mouse_xor.csv

rm $dir_output/$file_output

touch $dir_output/$file_output
echo "x, partial_y, fraction" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python3 $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -f $sensitivity >> $dir_output/$file_output
done