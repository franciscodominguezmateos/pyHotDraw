# -*- coding: utf-8 -*-

import math
import os
# Muestra solo 't' decimales, SIN redondear
def truncate(num, t):
    return math.floor(num * 10 ** t) / 10 ** t

def printArrow(g, x1, x2, y1, y2):
    alpha = math.atan2(y2 - y1, x2 - x1)
    k = 30
    xa = x2 - k * math.cos(alpha + 0.35)
    ya = y2 - k * math.sin(alpha + 0.35)
    g.drawLine(xa, ya, x2, y2)
    xa = x2 - k * math.cos(alpha - 0.35)
    ya = y2 - k * math.sin(alpha - 0.35)
    g.drawLine(xa, ya, x2, y2)

def addSheetStyle(w):
    p = os.path.dirname(os.path.abspath(__file__))
    qssFile = p + '/style.qss'
    with open(qssFile, "r") as fh:
        w.setStyleSheet(fh.read())

def is_float(v):
    try:
        float(v)
        return True
    except TypeError:
        return False
    except ValueError:
        return False



def crear_recta_a_partir_de_2_puntos(p0, p1):
    """
    http://www.mclibre.org/consultar/python/otros/formulas.html
    Calcula los valores de la pendiente(m) y del punto de corte al eje (n)
    que conforman una recta expresada como 'y=mx+n'.
    :param p0:
    :param p1:
    :return:
    """
    x1, y1 = p0.getX(), p0.getY()
    x2, y2 = p1.getX(), p1.getY()
    try:
        # y = mx + n
        m = (y2 - y1) / (x2 - x1)
        n = (x2*y1 - x1*y2) / (x2 - x1)
        return m, n
    except:
        return 0, 0

def distancia_punto_recta(m, n, p):
    """
    Calcula la distancia de un punto p (2D) a una recta expresada como
    y = mx+n. https://es.wikipedia.org/wiki/Distancia_de_un_punto_a_una_recta
    :param m: pendiente de la recta
    :param n: punto de intercepción en la ordenada
    :param p: punto
    :return: distancia (float) de p a la recta y=mx+n
    """
    x, y = p.getX(), p.getY()
    return abs(m*x - y + n) / math.sqrt(m**2 + 1)

