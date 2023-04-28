# This pipeline determines the elbow point of the network filtering process based on p-value.
# Author: Zhendong Sha 2023-04-28

#### Parameters ####
dir_target=res_purning
dir_output=kneed_point

dir_script=scr
file_script=identifyElbowPoint.py

sensitivity_begin=10
sensitivity_end=30
sensitivity_step=10

# save pwd to home
home=$(pwd)

#### Main ####

# for each file in the target folder

cd $dir_target
rm -rf $dir_output
mkdir -p $dir_output

# investigate the rat xor
echo "investigate the rat xor"
data=Rat_XOR2W_filtered.csv_networkInvestigation_pval.csv
file_output=elbow_rat_xor.csv

touch $dir_output/$file_output
echo "eblow, elbow_y, sensitivity" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python3 $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -curve concave -direction increasing -S $sensitivity >> $dir_output/$file_output
done


# investigate the rat cart
echo "investigate the rat cart"
data=Rat_Cart2W_filtered.csv_networkInvestigation_pval.csv
file_output=elbow_rat_cart.csv

touch $dir_output/$file_output
echo "eblow, elbow_y, sensitivity" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python3 $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -curve concave -direction increasing -S $sensitivity >> $dir_output/$file_output
done

# investigate the mouse xor
echo "investigate the mouse xor"
data=Mouse_XOR2W_filtered.csv_networkInvestigation_pval.csv
file_output=elbow_mouse_xor.csv

touch $dir_output/$file_output
echo "eblow, elbow_y, sensitivity" >> $dir_output/$file_output

for sensitivity in $(seq $sensitivity_begin $sensitivity_step $sensitivity_end)
do
    python3 $home/$dir_script/$file_script -input $data -x threshold -y modularity_greedy -curve concave -direction increasing -S $sensitivity >> $dir_output/$file_output
done