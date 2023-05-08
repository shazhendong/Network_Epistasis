# This file performs enrichment analysis based on gProfiler.
# Author: Zhendong Sha 2023-04-20

#### Parameters ####
dir_target=res_purning/network_filterings

dir_script=scr
file_script_rat=enrichment_rat.R
file_script_mouse=enrichment_mouse.R
file_script_splitList=divideSNPlistByCommunity.py

community_size_cutoff=50 # the minimum size of a community for enrichment analysis

# save pwd to home
home=$(pwd)

#### Main ####

# copy the enrichment script to the target folder
cp $home/$dir_script/$file_script_rat $dir_target
cp $home/$dir_script/$file_script_mouse $dir_target
cp $home/$dir_script/$file_script_splitList $dir_target

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
    
    # split the snp list by community
    python $file_script_splitList $file community $community_size_cutoff

    # if there is no file "$file"_community_*.csv generated, skip the following steps
    if [ ! -f "$file"_community_*.csv ]; then
        continue
    fi

    # iterate through the community files
    for community in "$file"_community_*.csv
    do
        # run the enrichment analysis
        echo $community
        # duplicate the file named enrichment.csv
        cp $community enrichment.csv
        Rscript $file_script_rat
        # remove the enrichment.csv
        rm enrichment.csv
        # rename the Terms.csv to $file.Terms.csv
        mv Terms.csv $community.Terms.csv
    done
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

    # split the snp list by community
    python $file_script_splitList $file community $community_size_cutoff

    # if there is no file "$file"_community_*.csv generated, skip the following steps
    if [ ! -f "$file"_community_*.csv ]; then
        continue
    fi

    # iterate through the community files
    for community in "$file"_community_*.csv
    do
        # run the enrichment analysis
        echo $community
        # duplicate the file named enrichment.csv
        cp $community enrichment.csv
        Rscript $file_script_rat
        # remove the enrichment.csv
        rm enrichment.csv
        # rename the Terms.csv to $file.Terms.csv
        mv Terms.csv $community.Terms.csv
    done
done

# clean up
rm $file_script_rat
rm $file_script_mouse
rm $file_script_splitList
