import fileinput
import json
import copy
import re
import math

def read_input():
    step = 0
    nodes = {}
    node_input = []
    data = []
    lines = []

    # Read file input and clean each line
    for line in fileinput.input():
        lines.append(line.strip())

    count = 0
    for line in lines:
        if '@attribute' in line and line[0] is not '%':
            count += 1
    total_attributes = count
    on_data = False
    for line in lines:
        # Lines that are not comments
        if not line or line[0] == '%':
            continue
        if '@data' in line:
            on_data = True
            continue
        if '@attribute' in line:
            count -= 1
            _, label, *rest = line.split(' ')
            nodes[label] = {}
            values = [re.sub(r'[ \{\},]','',value) for value in rest]
            nodes[label]['values'] = values
            node_input.append(label)
            if not count:
                nodes[label]['output'] = True       
        if on_data:
            data.append(line.split(','))

    return nodes, node_input, data

def get_entropy(data):
    posible_labels = { l: 0  for l in list(set(data)) }
    for value in data:
        posible_labels[value] += 1
    total = sum([ posible_labels[l] for l in posible_labels ])
    entropy = sum([ ((posible_labels[l]/total) * math.log2(posible_labels[l]/total)) for l in posible_labels ])
    return -1 * entropy

def get_information_gain(entropy, data):
    posible_values = { l: 0  for l in list(set(data)) }
    for value in data:
        posible_values[value] += 1
    total = sum([ posible_values[l] for l in posible_values ])

def get_value_list(data, index):
    if index == -1:
        return [ row[len(row) - 1] for row in data ]
    return [ row[index] for row in data ]

def generate_decision_tree(data, feature_names):
    # tree = {order ocurrence}
    print(feature_names)
    label_list = get_value_list(data, -1)
    system_entropy = get_entropy(label_list)
    print(system_entropy)
    # for label in labels:
        # print(l)
    # for row in data:
        # print(row[len(row) - 1])

def main():

    nodes, node_to_data, data = read_input()


    generate_decision_tree(data, node_to_data)

    # print(json.dumps(nodes, indent=2))
    # print(node_to_data)
    # for line in data:
    #     print(line)




if __name__ == '__main__':
    main()
