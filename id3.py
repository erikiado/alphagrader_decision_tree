import fileinput
import re
import math

nodes = {}

def read_input():
    step = 0
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
            rest = [ r for r in rest if r is not '' and r is not ' ' ]
            print(rest)
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
    total = len(data)
    posible_labels = { l: 0  for l in list(set(data)) }
    for value in data:
        posible_labels[value] += 1
    entropy = sum([ ((posible_labels[l]/total) * math.log2(posible_labels[l]/total)) for l in posible_labels ])
    return abs(entropy)


def get_posible_value_dict(data, labels):
    posible_values = { v: []  for v in list(set(data)) }
    for i, l in enumerate(labels):
        posible_values[data[i]].append(l)
    return posible_values


def get_information_gain(entropy, data, labels):
    total = len(data)
    posible_values = get_posible_value_dict(data, labels)
    sub_entropy = sum([ (get_entropy(posible_values[v]) * (len(posible_values[v])/total)) for v in posible_values ])
    return entropy - sub_entropy


def get_value_list(data, index):
    if index == -1:
        return [ row[len(row) - 1] for row in data ]
    return [ row[index] for row in data ]


def drop_column(data, index):
    neu_data = []
    for row in data:
        if index == -1:
            neu_data.append(row[:-1])
        else:
            neu_data.append(row[:index] + row[index + 1:])
    return neu_data


def get_most_information_gain(data, labels, feature_names, system_entropy):
    most_ig, most_index = -1.0, -1
    for j in range(len(feature_names)):
        column = get_value_list(data, j)
        current_ig = get_information_gain(system_entropy, column, labels)
        if current_ig > most_ig:
            most_ig, most_index = current_ig, j
    if most_index == -1:
        return None, -1, 0
    else:
        return feature_names[most_index], most_index, most_ig


def split_data(data, labels, feature_names, system_entropy, spaces):
    if len(set(labels)) == 1:
        print((' '*spaces) + 'ANSWER: ' + labels[0] )
        return
    feature, most_index, most_ig = get_most_information_gain(data, labels, feature_names, system_entropy)
    posibles = nodes[feature]['values'] # list(set(get_value_list(data,most_index)))
    for i, p in enumerate(posibles):
        sub = []
        n_labels = []
        for j, row in enumerate(data):
            if row[most_index] == p:
                sub.append(row)
                n_labels.append(labels[j])
        if feature:
            print((' '*spaces) + feature + ': ' +p)
        neu_names = feature_names[:most_index] + feature_names[most_index + 1:]
        split_data(sub, n_labels, feature_names, system_entropy, spaces+2)


def generate_decision_tree(data, feature_names):
    label_list = get_value_list(data, -1)
    label_name, feature_names = feature_names[-1], feature_names[:-1] 
    data = drop_column(data, -1)
    system_entropy = get_entropy(label_list)
    split_data(data, label_list, feature_names, system_entropy, 0)


def main():
    nodes, node_to_data, data = read_input()
    # generate_decision_tree(data, node_to_data)


if __name__ == '__main__':
    main()
