
from pyHotDraw.Tools.pyHAbstractTool import pyHAbstractTool

class AbstractTool(pyHAbstractTool):
    """
    Añade la funcionalidad de un método para realizar unas determinadas
    acciones al abandonar una Tool.
    """
    def exit(self, e=None):
        pass