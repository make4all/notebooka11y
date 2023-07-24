import json


class NotebookCell(object):
    cell_seq_num = 0
    fileNameState = ''

    cell_execution_order = "not implemented"
    cellType = None

    def __init__(self, filename, cellType):

        if NotebookCell.fileNameState != filename:
            NotebookCell.cell_seq_num = 0
            NotebookCell.fileNameState = filename

        self.cell_seq_num = NotebookCell.cell_seq_num
        NotebookCell.cell_seq_num += 1
        self.cellType = cellType

        self._has_output = False
        self._no_outputs = False
        self._output_contains_graphics = False
        self._output_contains_tables = False
        self._has_interactive = False
        self._has_heading = False
        self._has_links = False
        self._has_math_latex = False
        self._code_lines = None
        self._has_imports = False
        self._cell_execution_order = None
        self._num_h1 = 0
        self._num_h2 = 0
        self._num_h3 = 0
        self._num_h4 = 0
        self._num_h5 = 0
        self._num_h6 = 0
        self._num_tables = 0
        self._num_links = 0
        self._table_metadata = {}

    @property
    def cell_type(self):
        return self.cell_type

    @property
    def has_output(self):
        if self._has_output is None:
            raise ValueError("has_output is not set")
        return self._has_output

    @has_output.setter
    def has_output(self, value):
        self._has_output = bool(value)

    @property
    def no_outputs(self):
        if self._no_outputs is None:
            raise ValueError("no_outputs is not set")
        return self._no_outputs

    @no_outputs.setter
    def no_outputs(self, value):
        # must be an int
        if not isinstance(value, int):
            raise ValueError("no_outputs must be an int")
        self._no_outputs = value

    @property
    def output_contains_graphics(self):
        if self._output_contains_graphics is None:
            raise ValueError("output_contains_graphics is not set")
        return self._output_contains_graphics

    @output_contains_graphics.setter
    def output_contains_graphics(self, value):
        if not isinstance(value, bool):
            raise ValueError("output_contains_graphics must be a bool")
        self._output_contains_graphics = bool(value)

    @property
    def output_contains_tables(self):
        if self._output_contains_tables is None:
            raise ValueError("output_contains_tables is not set")
        return self._output_contains_tables

    @output_contains_tables.setter
    def output_contains_tables(self, value):
        if not isinstance(value, bool):
            raise ValueError("output_contains_tables must be a bool")
        self._output_contains_tables = bool(value)

    @property
    def has_interactive(self):
        if self._has_interactive is None:
            raise ValueError("has_interactive is not set")
        return self._has_interactive

    @has_interactive.setter
    def has_interactive(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_interactive must be a bool")
        self._has_interactive = bool(value)

    @property
    def has_heading(self):
        return self._has_heading

    @has_heading.setter
    def has_heading(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_heading must be a bool")
        self._has_heading = bool(value)

    @property
    def has_links(self):
        return self._has_links

    @has_links.setter
    def has_links(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_links must be a bool")
        self._has_links = bool(value)

    @property
    def has_math_latex(self):
        return self._has_math_latex

    @has_math_latex.setter
    def has_math_latex(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_math_latex must be a bool")
        self._has_math_latex = bool(value)

    @property
    def code_lines(self):
        if self._code_lines is None:
            raise ValueError("code_lines is not set")
        return self._code_lines

    @code_lines.setter
    def code_lines(self, value):
        if not isinstance(value, int):
            raise ValueError("code_lines must be an int")
        self._code_lines = value

    @property
    def has_imports(self):
        return self._has_imports

    @has_imports.setter
    def has_imports(self, value):
        if not isinstance(value, bool):
            raise ValueError("has_imports must be a bool")
        self._has_imports = bool(value)

    @property
    def cell_execution_order(self):
        return self._cell_execution_order

    @cell_execution_order.setter
    def cell_execution_order(self, value):
        self._cell_execution_order = value

    @property
    def num_h1(self):
        return self._num_h1

    @num_h1.setter
    def num_h1(self, value):
        self._num_h1 = value

    @property
    def num_h2(self):
        return self._num_h2

    @num_h2.setter
    def num_h2(self, value):
        self._num_h2 = value

    @property
    def num_h3(self):
        return self._num_h3

    @num_h3.setter
    def num_h3(self, value):
        self._num_h3 = value

    @property
    def num_h4(self):
        return self._num_h4

    @num_h4.setter
    def num_h4(self, value):
        self._num_h4 = value

    @property
    def num_h5(self):
        return self._num_h5

    @num_h5.setter
    def num_h5(self, value):
        self._num_h5 = value

    @property
    def num_h6(self):
        return self._num_h6

    @num_h6.setter
    def num_h6(self, value):
        self._num_h6 = value

    @property
    def num_tables(self):
        return self._num_tables

    @num_tables.setter
    def num_tables(self, value):
        return self._num_tables

    @property
    def table_metadata(self):
        return json.dumps(self._table_metadata)

    @table_metadata.setter
    def table_metadata(self, value):
        self._table_metadata = value

    @property
    def num_links(self):
        return self._num_links

    @num_links.setter
    def num_links(self, value):
        self._num_links = value