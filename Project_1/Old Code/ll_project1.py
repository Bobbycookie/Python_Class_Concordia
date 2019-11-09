import argparse
import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import pandas as pd


def generate_points(coefs, min_val, max_val):
    xs = np.arange(min_val, max_val, (max_val-min_val)/100)
    return xs, np.polyval(coefs, xs)

def convert_type(s):
    if element == "": # len(element) == 0
        return None
    try:
        return int(s)
    except ValueError:
        return s


def printkey(data,keydic):
    print(data.keys())
    print(data[keydic])

parser = argparse.ArgumentParser()
parser.add_argument("data_file",help="Input CSV data file for plotting")
parser.add_argument("-k ","--keyprint", type = str)                       
args = parser.parse_args()

rows = []

with open(args.data_file) as input_f: 
    rows = input_f.read()
    rows_1 = rows.split("\n")

outer_list = []
for row in rows_1:
    row_list = []
    for element in row.split(","):
        new_element = convert_type(element)
        if new_element is not None:
            row_list.append(new_element)
            # row_list += [new_element]   # equiv. to the above
        #print(element, end="\t")
        #print(new_element, type(new_element))
    #print(row_list)

    if len(row_list) > 0:
        outer_list += [row_list]

our_dictionary = {}

for location, column_headings in enumerate(outer_list[0]):
    print(column_headings)
    our_dictionary[column_headings] = list()  # equiv. to []
    for row in outer_list[1:]:
        our_dictionary[column_headings] += [row[location]]
    # Add data values to the corresponding columns

print(our_dictionary.keys())
#keyprint = input("choose key:",)
#print(our_dictionary[keyprint])
printkey(our_dictionary, keydic = args.keyprint)