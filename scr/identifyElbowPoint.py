# this py calculates the elbow point of the given data
# Parameters:
#   -input: the input data file (default: data.csv)
#   -x: the x axis of the data (default: x)
#   -y: the y axis of the data (default: y)
#   -curve: the curve of the data (convex or concave default: concave)
#   -direction: the direction of the data (decreasing or increasing default: increasing)
#   -S: the sensitivity of the elbow point (default: 100.0)
# Output:
#   elbow point, elbow point y value, sensitivity



# read the input parameters for each flag
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-input', type=str, default='data.csv')
parser.add_argument('-output', type=str, default='elbowPoint.csv')
parser.add_argument('-x', type=str, default='x')
parser.add_argument('-y', type=str, default='y')
parser.add_argument('-curve', type=str, default='concave')
parser.add_argument('-direction', type=str, default='increasing')
parser.add_argument('-S', type=float, default=100.0)

args = parser.parse_args()

# read the input data

import pandas as pd

data = pd.read_csv(args.input)


# get x and y axis

x = data[args.x].to_numpy()

y = data[args.y].to_numpy()

# get the elbow point

from kneed import KneeLocator

kn = KneeLocator(x, y, S=args.S, curve=args.curve, direction=args.direction)

# print the elbow point

print(kn.elbow, kn.elbow_y, args.S, sep=',')