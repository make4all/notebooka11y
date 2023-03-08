from enum import Enum

from regex import P



class CellType(Enum):
    CODE = "code"
    MARKDOWN = "markdown"

class NotebookCell:
    cell_seq_num = 0
    fileNameState = ''

    def __init__(self, filename,cellType):
        self.filename = filename
        if(NotebookCell.fileNameState != filename):
            NotebookCell.cell_seq_num = 0
            NotebookCell.fileNameState = filename

        self.cell_seq_num = NotebookCell.cell_seq_num
        NotebookCell.cell_seq_num += 1
        if CellType == "code":
            self.cell_type = CellType.CODE
        elif CellType == "markdown":
            self.cell_type = CellType.MARKDOWN
        else:
            raise ValueError("cell_type must be either 'code' or 'markdown'")
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

    @property
    def cell_type(self):
        return self.cell_type

    

    @property
    def has_output(self):
        if self._has_output == None:
            raise ValueError("has_output is not set")
        return self._has_output

    @has_output.setter
    def has_output(self, value):
        self._has_output = bool(value)

    @property
    def no_outputs(self):
        if self._no_outputs == None:
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
        if self._output_contains_graphics == None:
            raise ValueError("output_contains_graphics is not set")
        return self._output_contains_graphics

    @output_contains_graphics.setter
    def output_contains_graphics(self, value):
        if not isinstance(value, bool):
            raise ValueError("output_contains_graphics must be a bool")
        self._output_contains_graphics = bool(value)

    @property
    def output_contains_tables(self):
        if self._output_contains_tables == None:
            raise ValueError("output_contains_tables is not set")
        return self._output_contains_tables

    @output_contains_tables.setter
    def output_contains_tables(self, value):
        if not isinstance(value, bool):
            raise ValueError("output_contains_tables must be a bool")
        self._output_contains_tables = bool(value)

    @property
    def has_interactive(self):
        if self._has_interactive == None:
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
        if self._code_lines == None:
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
            @self.num_h5.setter
            def num_h5(self, value):
                self._num_h5 = value
            @property
            def num_h6(self):
                return self._num_h6
            @num_h6.setter
            def num_h6(self, value):
                self._num_h6 = value

    def to_dict(self):
        return {
            "filename": self.filename,
            "cell_seq_num": self.cell_seq,
            "cell_type": self.cell_type.value,
            "has_output": self.has_output,
            "no_outputs": self.no_outputs,
            "output_contains_graphics": self.output_contains_graphics,
            "output_contains_tables": self.output_contains_tables,
            "has_interactive": self.has_interactive,
            "has_heading": self.has_heading,
            "has_links": self.has_links,
            "has_math_latex": self.has_math_latex,
            "code_lines": self.code_lines,
            "num_h1": self.num_h1,
            "num_h2": self.num_h2,
            "num_h3": self.num_h3,
            "num_h4": self.num_h4,
            "num_h5": self.num_h5,
            "num_h6": self.num_h6
        }     
        
