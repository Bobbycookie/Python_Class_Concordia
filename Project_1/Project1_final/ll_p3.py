import re
import sys
import argparse
import csv
import collections 
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib
from matplotlib.pyplot import cm

#I have used the diabetes.data file as dataset
#ce fichier est celui avec le pair plot travailler sur celui la

def convert_type(element):
    # Case 2: is an emptry str, should be ignored
    if element == "": # len(element) == 0
        return None
    # Case 4: is a # with no ., should be int
    try:
        return int(element)
    except ValueError:
        return element

def checkdelim(rows):
    regex = re.compile(',') 
    if(regex.search(rows) == None): 
        #print("String does not contain this string")
        return False
        #print(aChecks)
        #print('Hello Boys')
          
    else: 
        #print("String contains this string")
        return True
        #print(aChecks)

def is_there_a_header(list_of_lists):
    for idx, col in enumerate(list_of_lists[0]):
        for row in list_of_lists:
            if type(row[idx]) is not type(col):
                return True
    return False

def generate_points(coefs, min_val, max_val):
    xs = np.arange(min_val, max_val, (max_val-min_val)/100)
    return xs, np.polyval(coefs, xs)

def discreete_data(data):
    perc_disc = 0.10
    maxnum = len(data)
    data_unique = Counter(data)
    single_num = len(data_unique.keys())
    single_perc = int(single_num/maxnum)
    print ("single",single_num)
    #print("data unique", data_unique)
    print("maxnum", maxnum)
    if single_perc <= perc_disc: 
        return True
    else: 
        return False

def pairClass (data, cols, polydeg = [1,2,3,4]):
    fig, ax = plt.subplots(figsize=(100, 100))
    ncols = len(data.keys())
        #fig = plt.Figure(figsize=(10, 10))
    for i1, column1 in enumerate(data.keys()):  # add enumerate and create i1 index
        for i2, column2 in enumerate(data.keys()):  # add enumerate and create i2 index
                #print(column1, column2)
            x = data[column1]
            y = data[column2]
            label = data[cols[0]]
            colors = ['red','green']
            #colorpoly = ['blue','red','green','orange']
            loc = i1*ncols + i2 + 1
            plt.subplot(ncols, ncols, loc)
            plt.title("{0} x {1}".format(column1, column2))
            plt.scatter(x, y, c=label, cmap= matplotlib.colors.ListedColormap(colors))
            
            for poly_order in polydeg:
                color=iter(cm.rainbow(np.linspace(0,1,poly_order)))
                c=next(color)
                coefs = np.polyfit(x, y, poly_order)  # we also want to do this for 2, 3
                f = np.poly1d(coefs)
                
                xs, new_line = generate_points(f, min(x), max(x))
                plt.plot(xs, new_line, c=c)
                plt.legend(polydeg,loc='upper right')
                        #Uncomment this line for the pairs plot
                        #plt.show()                
        
    
    plt.savefig("./my_pairs_plot.png")

def plotClass (data, cols):
    x = data[cols[0]]
    y = data[cols[1]]
    label = data[cols[2]]
    colors = ['red','green']
    
    fig = plt.figure(figsize=(5,5))
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.title("{0} x {1}".format(cols[0], cols[1]))
    #plt.plot(x, color='green')
    #plt.plot(y, color='red')
    plt.scatter(x, y, c=label, cmap= matplotlib.colors.ListedColormap(colors))

    #for poly_order in polydeg:
     #   coefs = np.polyfit(x, y, poly_order)  # we also want to do this for 2, 3
      #  f = np.poly1d(coefs)
       # xs, new_line = generate_points(f, min(x), max(x))
        #plt.savefig("./my_plot.png")
    plt.savefig("./my_regular_plot.png")
    plt.show()
    
        

parser = argparse.ArgumentParser()
parser.add_argument('fileA')
parser.add_argument('activdef', type = str)
parser.add_argument('-p',"--cplot", action="store_true")
parser.add_argument('-r',"--pplot", action="store_true")
parser.add_argument("--cols", nargs = '+', type = str)
parser.add_argument("--poly", type=int)
              
args = parser.parse_args()

rows = []
with open(args.fileA) as input_f: 
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

debug = False
print(our_dictionary.keys())

################# Run a function based on argparse ####################

#pairs plot
if args.activdef == "P":
    print ("pplot is printed")
    plotClass(our_dictionary, cols = args.cols)
else:
    print("pplot is inactive")

if args.activdef == "R":
    print ("pplot is printed")
    pairClass(our_dictionary, cols = args.cols)
else:
    print("pplot is inactive")

with open("myfile.csv", "w") as myCSV:
    w = csv.DictWriter(myCSV, our_dictionary.keys())
    w.writeheader()
    w.writerow(our_dictionary)
