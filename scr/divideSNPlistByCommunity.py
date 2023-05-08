# This python divide snp list by community, and write the result to file.
# Parameters:
#   1. snp list file (typical header: node,community,snp_gprofiler) Required
#   2. target column name (for example: community) Required
#   3. community size threshold (default: 50)

# output file is the same as input file, but divided by community (file name: snp list file_c).

# read snp list from file
import pandas as pd
import sys
df_snp = pd.read_csv(sys.argv[1], sep=',')

# get target column name
target_column_name = sys.argv[2]

# get community size threshold
if len(sys.argv) > 3:
    community_size_threshold = int(sys.argv[3])
else:
    community_size_threshold = 50

# divide df_snp into dfs by the value of target_column_name
print('dividing snp list into communities...')
df_snp_list = []
for i in df_snp[target_column_name].unique():
    df_snp_list.append(df_snp[df_snp[target_column_name] == i])

# filter out the dfs with size < community_size_threshold
print('filtering out communities with size < ' + str(community_size_threshold) + '...')
df_snp_list = [df for df in df_snp_list if len(df) >= community_size_threshold]

# if there is no community left, exit
if len(df_snp_list) == 0:
    print('no community left after filtering out communities with size < ' + str(community_size_threshold) + '...')
    sys.exit()

# get the community number of each df
print('getting community number of each community...')
community_number_list = [df[target_column_name].unique()[0] for df in df_snp_list]

# write the dfs to file
for i, df in enumerate(df_snp_list):
    print('writing community ' + str(community_number_list[i]) + ' to file...')
    df.to_csv(sys.argv[1] + '_community_' + str(community_number_list[i]) + '.csv', sep=',', index=False)
