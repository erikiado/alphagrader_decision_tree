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
    total = len(data)
    posible_labels = { l: 0  for l in list(set(data)) }
    for value in data:
        posible_labels[value] += 1
    entropy = sum([ ((posible_labels[l]/total) * math.log2(posible_labels[l]/total)) for l in posible_labels ])
    return abs(entropy)


def get_information_gain(entropy, data, labels):
    total = len(data)
    posible_values = get_posible_value_dict(data, labels)
    # for v in posible_values:
        # print('\t',get_entropy(posible_values[v])* (len(posible_values[v])/total))
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

def generate_decision_tree(data, feature_names):
    # tree = {order ocurrence}
    tree = {}
    label_list = get_value_list(data, -1)
    label_name, feature_names = feature_names[-1], feature_names[:-1] 
    data = drop_column(data, -1)
    system_entropy = get_entropy(label_list)
    # print('Entropy: ', system_entropy)

    order = []
    current_data = copy.deepcopy(data)
    current_feature_names = copy.deepcopy(feature_names)
    for i in range(len(feature_names)):
        most_ig, most_index = -1.0, -1
        for j in range(len(current_feature_names)):
            column = get_value_list(current_data, j)
            current_ig = get_information_gain(system_entropy, column, label_list)
            if current_ig > most_ig:
                most_ig, most_index = current_ig, j
                best_column = column
        tree[current_feature_names[most_index]] = { v:False for v in list(set(best_column))}
        order.append(current_feature_names[most_index])

        #obtener misma lista de correspondencia y ver los unique de cada attributo y si es uno ponerselo al valor en el arbol

        # RECURSIVAMENTE MIENTRAS HAYA INFORMACION DISPONIBLE EN DATA
        # CONSEGUIR COLUMNA CON MAYOR INFORMATION GAIN
        # AGREGAR AL ARBOL LA COLUMNA CON LOS VALORES DIRECTOS QUE DE 1
        # EN EL RESTO GUARDAR LA LISTA QUE CORRESPONDE A LOS LABELS DE ESA SEPARACION

        #tomar otra decicion o declarar respuesta
        current_data = drop_column(current_data, most_index)
        current_feature_names = current_feature_names[:most_index] + current_feature_names[most_index + 1:]
    print(json.dumps(tree, indent=2))



def main():

    nodes, node_to_data, data = read_input()

    generate_decision_tree(data, node_to_data)

    # print(json.dumps(nodes, indent=2))
    # print(node_to_data)
    # for line in data:
    #     print(line)




if _name_ == '_main_':
    main()
