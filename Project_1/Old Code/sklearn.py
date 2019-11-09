from sklearn.datasets import load_wine
import ll_p2

wine = load_wine()
target = wine.target
target = target.tolist()
# add 1 to target to make it like the .data file
target = [x+1 for x in target]
data = wine.data
data = data.tolist()
# combine target as column in data and add heading column
[data[idx].insert(0, target[idx]) for idx, item in enumerate(target)]
output_list, headers = my_script.check_for_headers(data)
# convert to dictionary
list_of_col_names = output_list.pop(0)
output_dict = [[row[i] for row in output_list] for i in range(len(list_of_col_names))]
output_dict = {list_of_col_names[idx]: item for idx, item in enumerate(output_dict)}
my_script.pairsplot(output_dict)

