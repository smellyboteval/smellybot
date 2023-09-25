import javalang as jl
import pandas as pd
import re

import warnings

# Disable all warnings
warnings.filterwarnings("ignore")


def __get_start_end_for_node(node_to_find, tree):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end

def __get_string(start, end, data):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain an additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string

def Extract(filename):
    methods = pd.DataFrame(columns=['Method'])
    classes = pd.DataFrame(columns=['Class'])
    
    try:
        data = open(filename).read()
        # Remove comments from the source code
        #data = remove_comments(data)
        tree = jl.parse.parse(data)
        
        for _, node in tree.filter(jl.tree.MethodDeclaration):
            start, end = __get_start_end_for_node(node, tree)
            #print('+++++++++++++++++', __get_string(start, end, data))
            methods = methods.append({'Method': __get_string(start, end, data)}, ignore_index=True)
        
        for _, node in tree.filter(jl.tree.ClassDeclaration):
            start, end = __get_start_end_for_node(node, tree)
            classes = classes.append({'Class': __get_string(start, end, data)}, ignore_index=True)

            
        
    except Exception as e:
        print("Error:", e, filename)
        
    return methods['Method'].values.tolist(), classes['Class'].values.tolist()

if __name__ == '__main__':
    methods, classes = Extract("Test/Java9BaseListener.java")
    
    print('Methods:')
    for method in methods:
        print(method)
    
    print('Classes:')
    for class_def in classes:
        print(class_def)
