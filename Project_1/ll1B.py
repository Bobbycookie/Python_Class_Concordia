import re
import sys
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np 

#I have used the diabetes.data file as dataset

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

parser = argparse.ArgumentParser()
#parser.add_argument('fileA', type=argparse.FileType('r'))
parser.add_argument('fileA')
args = parser.parse_args()


degreePoly = int(input("choose degree of polynomial ",))

rows = []

with open(args.fileA) as input_f: 
    rows = input_f.read()
    rows_1 = rows.split("\n")

outer_list = []
for row in rows_1:
    row_list = []
    for element in row.replace(" ",",").replace("  ",",").split(","):
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
keyprint = input("choose key:",)
print(our_dictionary[keyprint])

debug = False
if debug: #setting up the polynomial here
    number_combinations = 0
for column1 in our_dictionary.keys():
    for column2 in our_dictionary.keys():
        if debug:
            number_combinations += 1
            print(column1, column2)
                # import pdb
                # pdb.set_trace()
        else:
            x = our_dictionary[column1]
            y = our_dictionary[column2]
            rowsize = len(our_dictionary.keys())
            colsize = len(our_dictionary.values())
            print("rowsize=",rowsize)
            print("colsize=",colsize)

            plt.scatter(x, y)
            plt.xlabel(column1)
            plt.ylabel(column2)
            plt.title("{0} x {1}".format(column1, column2))

            coefs = np.polyfit(x, y, degreePoly)  # we also want to do this for 2, 3
            f = np.poly1d(coefs)
            #print(np.poly1d(f))
            xs, new_line = generate_points(f, min(x), max(x))
#           plt.plot(xs, new_line)
            plt.plot(xs, new_line, color="red")
            #xs, new_line = plt.subplots(rowsize,colsize)
            #Uncomment this line for the pairs plot
            plt.show()

#print(our_dictionary)
#split each string in list to get a lis of list and I use the function checkdelim to see which delimiter is used
with open("myfile.csv", "w") as myCSV:
    w = csv.DictWriter(myCSV, our_dictionary.keys())
    w.writeheader()
    w.writerow(our_dictionary)
