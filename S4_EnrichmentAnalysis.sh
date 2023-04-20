# This file performs enrichment analysis based on gProfiler.
# Author: Zhendong Sha 2023-04-20

#### Parameters ####
dir_target=res_purning/network_filterings

dir_script=scr
file_script_rat=enrichment_rat.R
file_script_mouse=enrichment_mouse.R

# save pwd to home
home=$(pwd)

#### Main ####

# copy the enrichment script to the target folder
cp $home/$dir_script/$file_script_rat $dir_target
cp $home/$dir_script/$file_script_mouse $dir_target

cd $dir_target

# analysis rat
# iterate through the snp lists of rat Rat*enrichment_*.csv
for file in Rat*enrichment_*.csv
do
    # run the enrichment analysis
    echo $file
    # duplicate the file named enrichment.csv
    cp $file enrichment.csv
    Rscript $file_script_rat
    # remove the enrichment.csv
    rm enrichment.csv
    # rename the Terms.csv to $file.Terms.csv
    mv Terms.csv $file.Terms.csv
done

# analysis mouse
# iterate through the snp lists of mouse Mouse*enrichment_*.csv
for file in Mouse*enrichment_*.csv
do
    # run the enrichment analysis
    echo $file
    # duplicate the file named enrichment.csv
    cp $file enrichment.csv
    Rscript $file_script_rat
    # remove the enrichment.csv
    rm enrichment.csv
    # rename the Terms.csv to $file.Terms.csv
    mv Terms.csv $file.Terms.csv
done

# clean up
rm $file_script_rat
rm $file_script_mouse
