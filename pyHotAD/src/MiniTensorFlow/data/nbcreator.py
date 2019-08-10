"""
http://nbformat.readthedocs.io/en/latest/format_description.html
"""

from nbformat import write as write_nb
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell, new_raw_cell
from nbformat.notebooknode import NotebookNode


class NotebookDocument(object):

    EXT = '.ipynb'

    def __init__(self):
        self._notebook = new_notebook()

    def __setitem__(self, key, value):
        self._notebook[key] = value

    def __getitem__(self, item):
        return self._notebook.get(item)

    def add_cell(self, cell):
        if isinstance(cell, NotebookNode):
            self._notebook['cells'].append(cell)
        elif isinstance(cell, _Cell):
            self._notebook['cells'].append(cell.get_cell())
        else:
            raise ValueError('Type of input cell is not valid')

    def save_notebook(self, path, add_ext=False):
            if add_ext:
                path += self.EXT
            try:
                write_nb(self._notebook, path)
                return True
            except IOError:
                print('Error creating the ipynb document')
                return False


class _Cell(object):

    def __init__(self, cell_type='code', content=''):
        if cell_type == 'code':
            self._cell = new_code_cell(str(content))
        elif cell_type == 'markdown':
            self._cell = new_markdown_cell(str(content))
        elif cell_type == 'raw':
            self._cell = new_raw_cell(str(content))
        else:
            raise ValueError("Unrecognized cell type: {}".format(cell_type))

    def __setitem__(self, key, value):
        self._cell[key] = value

    def __getitem__(self, item):
        return self._cell.get(item)

    def add_line(self, line):
        self._cell['source'] += str(line) + '\n'

    def get_cell(self):
        return self._cell


def code_cell(content=''):
    """
    Devuelve una nueva celda de codigo
    """
    return _Cell('code', content)


def markdown_cell(content=''):
    """
    Devuelve una nueva celda markdown
    """
    return _Cell('markdown', content)


def raw_cell(content=''):
    """
    Devuelve una nueva celda raw
    """
    return _Cell('raw', content)
