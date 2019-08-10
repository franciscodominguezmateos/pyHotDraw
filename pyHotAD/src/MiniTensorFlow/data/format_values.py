import numpy as np
from figures.MathTextFigure import format_matrix
import math


def is_float(v):
    try:
        float(v)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def is_negative(v):
    if is_float(v):
        return float(v) < 0
    raise ValueError('{} is not float'.format(type(v)))

def is_matrix(v):
    """
    Comprueba si un valor es una matriz que contiene más de 1 elemento
    """
    return (isinstance(v, np.matrix) and v.size > 1) or \
           (isinstance(v, list) and len(v) > 1)


def format_number(v):
    return str(truncate(float(v), 3))

def format_value(v):
    if is_float(v):
        return format_number(v)
    elif is_matrix(v):
        return format_matrix(v)
    return str(v)


def truncate(num, d):
    """
    Muestra solo 'd' decimales, SIN redondear
    :param num: numero de entrada
    :param d: decimales máximos a mostrar
    :return:
    """
    return math.floor(num * 10 ** d) / 10 ** d