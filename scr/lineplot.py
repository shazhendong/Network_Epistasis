# this py file is to plot the line chart of the data (-f). the column of the x-axis and y-axis are defined by the user using flags -x and -y.

import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--xaxis", help="the column name of the x-axis")
parser.add_argument("-y", "--yaxis", help="the column name of the y-axis")
parser.add_argument("-i", "--file", help="the file name of the data")

args = parser.parse_args()

df = pd.read_csv(args.file)
df.plot(x=args.xaxis, y=args.yaxis)
# save the plot as a pdf file named "lineplot.pdf"
plt.savefig("lineplot.pdf")