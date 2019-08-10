import numpy as np

ARGS_ERROR = 'Input type must be: \n' + \
       '- vector(vector) \n ' + \
       '- vector(list) \n ' + \
       '- vector(float, float) \n ' + \
       '- vector(float, float, float)'

LIST_ARG_ERROR = 'List must be contain numbers'

class vector:
    """
    Class vector basada en la clase vector de vphython. http://www.vpython.org/contents/docs_vp5/visual/vector.html
    Implementación para suplir su ausencia en python 3, dado que solo existe
    para documentos jupyter notebook
    """
    def __init__(self, *args):
        self._vector = np.zeros(3, np.float64)
        if args:
            args_len = len(args)
            if args_len == 1:
                if isinstance(args[0], vector):
                    self._ctor_vector(args[0])
                elif type(args[0]) in (list, np.ndarray, tuple) and 2 <= len(args[0]) <= 3:
                    self._ctor_list(args[0])
                else:
                    raise TypeError(ARGS_ERROR)

            elif 2 <= args_len <= 3:
                self._ctor_numbers(args, args_len)

            else:
                raise TypeError(ARGS_ERROR)


    def _ctor_numbers(self, args, args_len):
        self.setX(np.float64(args[0]))
        self.setY(np.float64(args[1]))
        if args_len == 3: self.setZ(np.float64(args[2]))

    def _ctor_list(self, number_list):
        try:
            self._ctor_numbers(number_list, len(number_list))
        except TypeError(LIST_ARG_ERROR):
            pass

    def _ctor_vector(self, v):
        self.setX(v.x)
        self.setY(v.y)
        self.setZ(v.z)

    # Acceso a los componentes x, y, z
    def setX(self, value):
        self._vector[0] = np.float64(value)

    def setY(self, value):
        self._vector[1] = np.float64(value)

    def setZ(self, value):
        self._vector[2] = np.float64(value)

    def getX(self):
        return self._vector[0]

    def getY(self):
        return self._vector[1]

    def getZ(self):
        return self._vector[2]

    # https://docs.python.org/3/library/functions.html#property
    x = property(getX, setX)
    y = property(getY, setY)
    z = property(getZ, setZ)

    def components(self):
        return self._vector

    def toList(self):
        return self._vector.tolist()

    def __iter__(self):
        return iter(self.components())

    # operaciones sobre el vector
    def mag(self):
        return np.linalg.norm(self._vector)

    def mag2(self):
        return self.mag()**2

    def norm(self):
        v_copy = self._vector.copy()
        if self.mag() != 0:
            v_copy /= self.mag()
        return vector(v_copy)

    def cross(self, vec):
        cross_vec = np.cross(self.components(), vec.components())
        return vector(cross_vec)

    def dot(self, vec):
        return self._vector.dot(vec.components())


    def __add__(self, other):
        return vector(self.components() + other.components())

    def __sub__(self, other):
        return vector(self.components() - other.components())

    def __mul__(self, other):
        if isinstance(other, vector):
            return self.dot(other)
        elif isinstance(other, (int, float)):
            return vector(self.components() * other)
        else:
            raise ValueError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.x == other.x and\
               self.y == other.y and\
               self.z == other.z

    # vector[0] -> x, vector[1] -> y, vector[2] -> z
    def __getitem__(self, item):
        i = int(item)
        return self._vector[i]

    # print (v)
    def __str__(self):
        """
        https://stackoverflow.com/questions/385325/dropping-trailing-0-from-floats
        :return:
        """
        return '<{0:g} {1:g} {2:g}>'.format(self.x,
                                            self.y,
                                            self.z)

    def __repr__(self):
        return 'vector({} {} {})'.format(self.x, self.y, self.z)


