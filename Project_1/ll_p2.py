import re
import sys
import argparse
import csv
import collections 
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np 
import statistics 
from statistics import mean,median,mode

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

def plotting_pair(data, debug = False,pplot = False, polyDeg = [1,2,3,4]):
    fig, ax = plt.subplots(figsize=(100, 100))
    ncols = len(data.keys())
        #fig = plt.Figure(figsize=(10, 10))
    for i1, column1 in enumerate(data.keys()):  # add enumerate and create i1 index
        for i2, column2 in enumerate(data.keys()):  # add enumerate and create i2 index
                #print(column1, column2)

            x = data[column1]
            y = data[column2]
                    #rowsize = len(data.keys())
                    #colsize = len(data.values())
                    #print("rowsize=",rowsize)
                    #print("colsize=",colsize)

            loc = i1*ncols + i2 + 1
            plt.subplot(ncols, ncols, loc)
            plt.scatter(x, y)
            plt.title("{0} x {1}".format(column1, column2))

            for poly_order in polyDeg:
                coefs = np.polyfit(x, y, poly_order)  # we also want to do this for 2, 3
                f = np.poly1d(coefs)
                xs, new_line = generate_points(f, min(x), max(x))
        #               plt.plot(xs, new_line)
                plt.plot(xs, new_line, color="red")
                        #Uncomment this line for the pairs plot
                        #plt.show()                
        
    plt.legend()
    plt.savefig("./my_pairs_plotB.png")

def plot_regular(data,polydeg, activR = False):
    print("prouti debug")
    for cols1 in data.keys():
        for cols2 in data.keys():
            x = data[cols1]
            y = data[cols2]
            rowsize = len(data.keys())
            colsize = len(data.values())
                                #print("rowsize=",rowsize)
                                #print("colsize=",colsize)
            plt.scatter(x, y)
            plt.xlabel(cols1)
            plt.ylabel(cols2)
            plt.title("{0} x {1}".format(cols1, cols2))

            coefs = np.polyfit(x, y, polydeg)  # we also want to do this for 2, 3
            f = np.poly1d(coefs)
            xs, new_line = generate_points(f, min(x), max(x))
            plt.plot(xs, new_line, color="red")
            plt.savefig("./my_plot.png")
            plt.show()
            print("prouti")

def plot_summary(data, summary):
    
    assert summary in data.keys() , 'column name does not exist'
    for k in data.keys():
        if k == summary:
            yep = data[k]
    if len(np.unique(yep))/len(yep) <  0.1:
        print('Column is categorical/discrete')
    else:
            print('Column is continuous')      
    print('min is '+ str(min(yep)))
    print('max is ' + str(max(yep)))
    print('mean is ' + str(np.mean(yep)))
    print('std is ' + str(np.std(yep)))

def interpolation(data, interpolate, activI = False):
    #column1 = input("type name of first column: ",)
    #column2 = input("type name of second column: ",)
    #value_inp = input('enter a value: ',)
    #poly_degree = int(input("Enter a degree for you polynomial (INT ONLY): ",))
    if activI:
        if interpolate[0] not in data.keys():
            print("Column 1 is not in the list")
            sys.exit()
        elif interpolate[1] not in data.keys():
            print("Column 2 is not in the list")
            sys.exit()

        x = data[interpolate[0]]
        y = data[interpolate[1]]
            # polynomial 1
        d1 = np.polyfit(x, y, 1)
        d1_val = np.polyval(d1, convert_type(interpolate[2]))
        print("Value 1: {}".format(d1_val))
            # polynomial 2
        d2 = np.polyfit(x, y, 2)
        d2_val = np.polyval(d2, convert_type(interpolate[2]))
        print("Value 2: {}".format(d2_val))
            # polynomial 3
        d3 = np.polyfit(x, y, 3)
        d3_val = np.polyval(d3, convert_type(interpolate[2]))
        #plt.plot(x,y,v3_val)
        #plt.show()
        print("Value 3: {}" .format(d3_val))

def plotClass (data, cols, cat_class):
    for cat_class in data.keys():
        SortC = data[cat_class]
        

parser = argparse.ArgumentParser()
parser.add_argument('fileA')
parser.add_argument('activdef', type = str)
parser.add_argument("--cols", nargs = 3, type = str)
parser.add_argument("--class", type=str)
parser.add_argument('-s', '--summary', type = str, help="Type the key and displays Min/Max/Mean")
parser.add_argument('-p', '--pplot', action="store_true", help="Save Pair Plot")
parser.add_argument('-r', '--rplot', type = int, help="Display plot figure") 
parser.add_argument('-i','--interpolation', nargs = 3, help= "enter 2 columns name and 1 value, in this order!")               
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
    plotting_pair(our_dictionary)
else:
    print("pplot is inactive")

#Summary check
if args.activdef == "S":
    print ("Summary is printed")
    plot_summary(our_dictionary,summary=args.summary)
else: 
    print("Summary is inactive")

#Interpolate check
if args.activdef == "I":
    print ("Interpolate is printed")
    interpolation(our_dictionary, interpolate = args.interpolation)
else : 
    print("Interpolate is inactive")
#value_inp must be an int

#Only Plotting 
if args.activdef == "R":
    print("Regular plot is printed")
    plot_regular(our_dictionary,polydeg = args.rplot, cols = args.cols)
else: 
    print("Regular plot is inactive")


with open("myfile.csv", "w") as myCSV:
    w = csv.DictWriter(myCSV, our_dictionary.keys())
    w.writeheader()
    w.writerow(our_dictionary)

###########################################################
#UNUSED CODE
#plotting(different_dictionary)
#print(our_dictionary)
#split each string in list to get a lis of list and I use the function checkdelim to see which delimiter is used
#parser.add_argument('fileA', type=argparse.FileType('r'))
# plt.xlabel(column1)
# plt.ylabel(column2)
#print(np.poly1d(f))
#testKeyA = input("testKeyA= ",)
#testKeyB = input("testKeyB= ",)
#print("testA ", our_dictionary[testKeyA])
#print("testB ", our_dictionary[testKeyB])
#print (our_dictionary)
    # Add data values to the corresponding columns
     #print(data.keys())
    #Col1 = input("choose a key: ",)
    #while Col1 not in data.keys():
    #    Col1 = input("retry, choose a key: ",)
    #if Col1 in data.keys():
     #       #print(data[Col1])
      #      print("the max is:", max(data[Col1]))
       #     print("the min is:", min(data[Col1]))
        #    print("the mean is:", mean(data[Col1]))
         #   discreete_data(data)
          #  d_data = discreete_data(data)
           # print ("{} of your data is discreete".format(d_data))