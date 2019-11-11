import argparse
import sys
import csv
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

def pandaplot(fileA,cols):
    data_file = pd.read_csv(fileA)
    for header in data_file.columns:
        color=['red','green']

        groups = header.groupby(cols[0])

        fig, ax = plt.subplots(figsize=(11,8))

        for name, group in groups:   
            for x in group.values:
                if np.isnan(x[4]):
                    ax.plot(x[1], x[2], marker='x', linestyle='', ms=12)
                else:
                    ax.plot(x[1], x[2], marker='o', linestyle='', ms=12)                       

        #ax.legend()
        #df.plot()
        plt.show()

parser = argparse.ArgumentParser()
parser.add_argument('fileA')
parser.add_argument('-c', '--cols', nargs = 1)
args = parser.parse_args()

pandaplot (fileA= args.fileA, cols=args.cols)