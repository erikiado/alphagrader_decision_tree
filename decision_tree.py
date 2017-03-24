import fileinput
import json
import copy
import re


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




def main():

    nodes, node_to_data, data = read_input()

    print(json.dumps(nodes, indent=2))
    print(node_to_data)
    for line in data:
        print(line)




if _name_ == '_main_':
    main()