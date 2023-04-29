# this py calculates a partial optimal cutoff
# Parameters:
#   -input: the input data file (default: data.csv)
#   -x: the x axis of the data (default: x)
#   -y: the y axis of the data (default: y)
#   -f: the fraction of the optimal cutoff (default: 0.9)
# Output:
#   x, y value, fraction



# read the input parameters for each flag
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-input', type=str, default='data.csv')
parser.add_argument('-x', type=str, default='x')
parser.add_argument('-y', type=str, default='y')
parser.add_argument('-f', type=float, default=0.9)


args = parser.parse_args()

# read the input data

import pandas as pd

data = pd.read_csv(args.input)


# get x and y axis

x = data[args.x].to_numpy()

y = data[args.y].to_numpy()

# get the cutoff

target_y = y.max() * args.f

for i in range(len(y)):
    if y[i] >= target_y:
        # print the cutoff, y value, and the fraction
        print(x[i], y[i], args.f, sep=',')
        break

# print the cutoff
