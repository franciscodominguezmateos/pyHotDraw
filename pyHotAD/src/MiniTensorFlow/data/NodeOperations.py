

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from sorts import topological

# Solo letra
def showInfoFunctionLetter():
    pass

# Ventana creacion
def showInfoFunctionType(node_list):
    for n in node_list:
        if not n.is_input():
            op = n.get_operation()
            n.set_text(op)

# Letra de funcion + Tipo de funcion (subindice)
def showInfoHybrid(node_list):
    for n in node_list:
        if not n.is_input():
            letter = n.get_function_letter()
            op = n.get_operation()
            text = letter + '_{_{' + op + '}}'
            n.set_text(text)

def topological_sort(node_list):
    graph = {n: n.get_outputs_nodes() for n in node_list}
    return topological(graph)
