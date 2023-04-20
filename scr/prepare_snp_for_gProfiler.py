# this py transforms the snp column (chr:pos) of a csv file into a g:profiler ready column (chr:pos-range:pos+range).
# Parameters:
# -i: input file
# -o: output file
# -r: range (default 1000)
# -c: target column name (default snp)

import argparse
import pandas as pd

# read parameters
parser = argparse.ArgumentParser(description='Prepare SNP column for g:profiler')
parser.add_argument('-i', '--input', help='Input file', required=True)
parser.add_argument('-o', '--output', help='Output file', required=True)
parser.add_argument('-r', '--range', help='Range', required=False, default=1000)
parser.add_argument('-c', '--column', help='Target column', required=False, default='snp')

args = parser.parse_args()

# read input file
df = pd.read_csv(args.input, sep=',')

# get snp column
snps = df[args.column]

# split snp column into chr and pos. for example from chr15.7489086_G to 15 and 7489086
chr = snps.str.split('.').str[0].str.split('chr').str[1]
pos = snps.str.split('.').str[1].str.split('_').str[0]

# create new column with chr:pos-range:pos+range with the column name snp_gprofiler_$args.range
df['snp_gprofiler_' + str(args.range)] = chr + ':' + (pos.astype(int) - int(args.range)).astype(str) + ':' + (pos.astype(int) + int(args.range)).astype(str)

# write output file
df.to_csv(args.output, sep=',', index=False)