# This pipeline visualize all the network investigation results in the target folder
# Author: Zhendong Sha 2023-03-20

#### Parameters ####
dir_target=res_purning
dir_output=visualization

dir_script=scr
file_script=lineplot.py

# save pwd to home
home=$(pwd)

#### Main ####

# for each file in the target folder

cd $dir_target
rm -rf $dir_output
mkdir -p $dir_output

for f in *.csv
do
    file=${f%.*}
    echo $file
    mkdir -p $dir_output/$file
    dir_output_file=$dir_output/$file
    # visualize num_nodes vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "num_nodes"
    mv lineplot.pdf $dir_output_file/"$file"_num_nodes_vs_threshold.pdf
    # visualize num_edges vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "num_edges"
    mv lineplot.pdf $dir_output_file/"$file"_num_edges_vs_threshold.pdf
    # visualize num_components vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "num_components"
    mv lineplot.pdf $dir_output_file/"$file"_num_components_vs_threshold.pdf
    # visualize size_largest_component vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "size_largest_component"
    mv lineplot.pdf $dir_output_file/"$file"_size_largest_component_vs_threshold.pdf
    # visualize num_triangles vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "num_triangles"
    mv lineplot.pdf $dir_output_file/"$file"_num_triangles_vs_threshold.pdf
    # visualize modularity_greedy vs threshold
    python $home/$dir_script/$file_script -i "$file.csv" -x "threshold" -y "modularity_greedy"
    mv lineplot.pdf $dir_output_file/"$file"_modularity_greedy_vs_threshold.pdf
done

