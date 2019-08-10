import numpy as np

from MiniTensorFlow.figures.MathTextFigure import MathTextFigure
from pyHotDraw.Figures.pyHAttributes import *
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure

MARGIN = 40
_MARGIN = {1: 10,
           2: 20,
           3: 30}

ACCEPTABLE_TYPES = (list, np.ndarray, np.matrix)

class MatrixFigure(pyHCompositeFigure):
    """
        Example data: [['x_{_{0,0}}', '\cdots', 'x_{_{0,j}}'],
                       ['\\vdots',    '\ddots', '\\vdots'],
                       ['x_{_{i,0}}', '\cdots', 'x_{_{i,j}}']]

        Exmaple 2: numpy.array([1, 2, 3], numpy.float32)
    """
    def __init__(self, x, y, data=None, font_size=15):
        """

        :param x: posición x en el dibujo
        :param y: posición y en el dibujo
        :param data: lista de elemntos de la matriz
        :param font_size: tamaño de fuente de los elementos de la matriz
        """
        pyHCompositeFigure.__init__(self)
        # superclass call
        if not isinstance(data, ACCEPTABLE_TYPES):
            raise TypeError

        self.x0 = x
        self.y0 = y
        self.w = 0
        self.h = 0

        self._font_size = font_size
        self._data = self._crear_valor_data(data)
        self._ARC_MARGIN = 20
        self.initialization()

    def _is_vector(self):
        """
        Comprueba si el dato es una array de 1 dimensión.
        Ejemplo:
        _is_vector( [1, 2, 3] )       : True
        _is_vector( [[1, 2, 3]] )     : True
        _is_vector( [[1], [2], [3]] ) : False
        :return:
        """
        return len(self._data.shape) == 1

    @staticmethod
    def _crear_valor_data(data):
        """

        :param data:
        :return:
        """
        if data is not None:
            if isinstance(data, np.matrix):
                data_as_np = data.A
            else:
                data_as_np = np.array(data)

            if len(data_as_np.shape) == 1:
                return np.array([data])
            else:
                return data_as_np
        else:
            return np.array([])

    def initialization(self):
        #crear figuras
        h_max, w_max, math_figures = self._crear_elementos_de_la_matriz()
        self._posicionar_elementos_de_la_matriz(h_max, w_max, math_figures)

        h, w = self._data.shape
        self.w = w * w_max
        self.h = h * h_max

        left_arc, right_arc = self._create_brackets(self._ARC_MARGIN)
        self.addFigure(left_arc)
        self.addFigure(right_arc)

        self._add_conteiner()

    def _crear_elementos_de_la_matriz(self):
        w_max = 0
        h_max = 0
        math_figures = []
        h, w = self._data.shape

        for f in reversed(range(h)):
            for c in range(w):
                math_figure = MathTextFigure(self.x0, self.y0)
                math_figure.set_math_text(self._data[f][c], self._font_size)
                math_figure.setAttribute('COLOR', pyHAttributeColor(0, 0, 0, 0))
                math_figure.setAttribute('FILL',
                                         pyHAttributeFillColor(0, 0, 0, 0))
                math_figures.append(math_figure)
                if math_figure.w > w_max: w_max = math_figure.w
                if math_figure.h * 0.7 > h_max: h_max = math_figure.h * 0.7

        return h_max, w_max, math_figures

    def _posicionar_elementos_de_la_matriz(self, h_max, w_max, math_figures):
        h, w = self._data.shape
        for posicion_fila in reversed(range(h)):
            for posicion_columna in range(w):
                math_figure = math_figures.pop(0)
                math_figure.x0 = self.x0 + posicion_columna * w_max + \
                                 (w_max - math_figure.w) / 2
                math_figure.y0 = self.y0 + (h - 1 - posicion_fila) * h_max + \
                                 (h_max - math_figure.h) / 2
                self.addFigure(math_figure)

    def _create_brackets(self, arc_width):
        arc_dcho = _Bracket(self.x + self.w - self._ARC_MARGIN + 3, self.y0,
                            arc_width, self.h, -90, 90)
        arc_izq = _Bracket(self.x, self.y,
                           arc_width, self.h, 90, -90)
        return arc_izq, arc_dcho


    def _add_conteiner(self):
        margin = 10
        old_x = self.x0
        old_y = self.y0
        self.move(margin, margin*2)

        conteiner = pyHRectangleFigure(old_x, old_y,
                               self.getWidth() + 2*margin,
                               self.getHeight() + 2*margin)
        print('contenedor: {} - {}'.format(self.w, self.getWidth()))
        conteiner.setAttribute('WIDTH', pyHAttributeWidth(2))
        conteiner.setAttribute('COLOR', pyHAttributeColor(150, 150, 150))
        conteiner.setAttribute('FILL', pyHAttributeFillColor(255, 255, 255))
        self.figures.insert(0, conteiner)


    def get_data(self):
        return self._data

    def setX(self, x):
        x = int(x)
        self.move(x - self.x0, 0)
        self.x0 = x

    def setY(self, y):
        y = int(y)
        self.move(0, y - self.y0)
        self.y0 = y

    def getX(self):
        return self.x0

    def getY(self):
        return self.y0

    x = property(getX, setX)
    y = property(getY, setY)

    def getHeight(self):
        return self.getDisplayBox().getHeight()

    def getWidth(self):
        return self.getDisplayBox().getWidth()

    def getConteinerFigure(self):
        return self.getFigures()[0]

    def getBracketsFigures(self):
        return self.getFigures()[-3:-1]

    def setAttribute(self,k,v):
        self.getFigures()[0].setAttribute(k, v)

    def addChangedFigureObserver(self,fo):
        for f in self.getFigures():
            f.addChangedFigureObserver(fo)

from pyHArcFigure import pyHArcFigure

class _Bracket(pyHArcFigure):
    def __init__(self, x, y, w, h, ane, ans):
        self._ARC_WIDTH = w
        self._ARC_HEIGHT = h
        pyHArcFigure.__init__(self, x, y, self._ARC_WIDTH,
                              self._ARC_HEIGHT, ane, ans)
        self.setAttribute('WIDTH', pyHAttributeWidth(1.5))

    def move(self,dx,dy):
        pyHArcFigure.move(self, dx, dy)
        self.arc.setWidth(self._ARC_WIDTH)
        self.arc.setHeight(self._ARC_HEIGHT)

