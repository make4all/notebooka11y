import json


class NotebookCell(object):
    """
    A class used to represent the jupyter notebook cell

    ...

    Attributes
    ----------
    cell_seq_num : int
        Sequence number of cells (default 0)
    fileNameState : str
        Current file name (default '')
    cell_execution_order : str
        Cell execution order (default "not implemented")
    cellType : NoneType
        Type of cell (default None)

    Methods
    -------
    cell_type()
        Returns the type of cell
    has_output()
        Returns the cell output
    has_output(value)
        To set the cell output
    no_outputs()
        Returns the number of outputs for the given cell    
    no_outputs(value)
        Sets the number of associated outputs count to the cell
    output_contains_graphics()
        Returns the status of whether or not the cell contains graphics
    output_contains_graphics(value)
        Sets the status of whether or not the cell contains graphics 
    output_contains_tables()
        Returns the status of whether or not the output contain any tables
    output_contains_tables(value)
        Sets the status of whether or not the output contains any tables
    has_interactive()
        Returns the status of whether or not the cell has an interactive element 
    has_interactive(value)
        Sets the status of whether or not the cell has an interactive element
    has_heading()
        Returns the status of whether or not the cell has any headings
    has_heading(value)
        Sets the status of whether or not the cell has any headings 
    has_links()
        Returns the status of whether or not the cell has any links 
    has_links(value)
        Sets the status of whether or not the cell has any links
    has_math_latex()
        Returns the status of whether or not the cell contains any math latex
    has_math_latex(value)
        Sets the status of whether or not the cell contains any math latex
    code_lines()
        Returns the number of lines that are present in the current code cell
    code_lines(value)
        Sets the number of lines that present codes in the cell 
    has_imports()
        Returns the status of whether or not the cell contains any imports
    has_imports(value)
        Sets the status of whether or not the cell contains any math latex
    cell_execution_order()
        Returns the execution order number of the cell
    cell_execution_order(value)
        Sets the execution order number of the cell
    num_h1()
        Returns the number of the heading level 1 in the cell (H1)
    num_h1(value)
        Sets the number of the heading level 1 in the cell (H1)
    num_h2()
        Returns the number of the heading level 2 in the cell (H2)
    num_h2(value)
        Sets the number of the heading level 2 in the cell (H2)
    num_h3()
        Returns the number of the heading level 3 in the cell (H3)
    num_h3(value)
        Sets the number of the heading level 3 in the cell (H3)
    num_h4()
        Returns the number of the heading level 4 in the cell (H4)
    num_h4(value)
        Sets the number of the heading level 4 in the cell (H4)
    num_h5()
        Returns the number of the heading level 5 in the cell (H5)
    num_h5(value)
        Sets the number of the heading level 5 in the cell (H5)
    num_h6()
        Returns the number of the heading level 6 in the cell (H6)
    num_h6(value)
        Sets the number of the heading level 6 in the cell (H6)
    """


    cell_seq_num = 0
    fileNameState = ''

    cell_execution_order = "not implemented"
    cellType = None

    def __init__(self, filename, cellType):
        """
        Parameters
        ----------
        filename : str
            The name of the file
        cellType : NoneType
            Type of cell
        """
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
        '''
        Returns the type of cell
        '''
        return self.cell_type

    @property
    def has_output(self):
        '''
        Returns the cell output

        Raises
        ------
        ValueError
            If has_output is not set
        '''
        if self._has_output is None:
            raise ValueError("has_output is not set")
        return self._has_output

    @has_output.setter
    def has_output(self, value):
        '''
        To set the cell output
        '''
        self._has_output = bool(value)

    @property
    def no_outputs(self):
        '''
        Returns the number of associated outputs with a given cell

        Raises
        ------
        ValueError
            If no_outputs is not set
        '''
        if self._no_outputs is None:
            raise ValueError("no_outputs is not set")
        return self._no_outputs

    @no_outputs.setter
    def no_outputs(self, value):
        '''
        Sets the number of outputs associated with a given cell

        Raises
        ------
        ValueError
            If no_outputs is not set in the int type
        '''
        # must be an int
        if not isinstance(value, int):
            raise ValueError("no_outputs must be an int")
        self._no_outputs = value

    @property
    def output_contains_graphics(self):
        '''
        Returns the status of whether or not the cell contains graphics

        Raises
        ------
        ValueError
            If output_contains_graphics is not set
        '''
        if self._output_contains_graphics is None:
            raise ValueError("output_contains_graphics is not set")
        return self._output_contains_graphics

    @output_contains_graphics.setter
    def output_contains_graphics(self, value):
        '''
        Sets the status of whether or not the cell contains graphics 

        Raises
        ------
        ValueError
            If output_contains_graphics is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("output_contains_graphics must be a bool")
        self._output_contains_graphics = bool(value)

    @property
    def output_contains_tables(self):
        '''
        Returns the status of whether or not the output contain any tables

        Raises
        ------
        ValueError
            If output_contains_tables is not yet set
        '''
        if self._output_contains_tables is None:
            raise ValueError("output_contains_tables is not set")
        return self._output_contains_tables

    @output_contains_tables.setter
    def output_contains_tables(self, value):
        '''
        Sets the status of whether or not the output contains any tables

        Raises
        ------
        ValueError
            If output_contains_tables is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("output_contains_tables must be a bool")
        self._output_contains_tables = bool(value)

    @property
    def has_interactive(self):
        '''
        Returns the status of whether or not the cell has an interactive element 

        Raises
        ------
        ValueError
            If has_interactive is not yet set
        '''
        if self._has_interactive is None:
            raise ValueError("has_interactive is not set")
        return self._has_interactive

    @has_interactive.setter
    def has_interactive(self, value):
        '''
        Sets the status of whether or not the cell has an interactive element

        Raises
        ------
        ValueError
            If has_interactive is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("has_interactive must be a bool")
        self._has_interactive = bool(value)

    @property
    def has_heading(self):
        '''
        Returns the status of whether or not the cell has any headings
        '''
        return self._has_heading

    @has_heading.setter
    def has_heading(self, value):
        '''
        Sets the status of whether or not the cell has any headings 

        Raises
        ------
        ValueError
            If has_heading is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("has_heading must be a bool")
        self._has_heading = bool(value)

    @property
    def has_links(self):
        '''
        Returns the status of whether or not the cell has any links 
        '''
        return self._has_links

    @has_links.setter
    def has_links(self, value):
        '''
        Sets the status of whether or not the cell has any links

        Raises
        ------
        ValueError
            If has_links is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("has_links must be a bool")
        self._has_links = bool(value)

    @property
    def has_math_latex(self):
        '''
        Returns the status of whether or not the cell contains any math latex
        '''
        return self._has_math_latex

    @has_math_latex.setter
    def has_math_latex(self, value):
        '''
        Sets the status of whether or not the cell contains any math latex

        Raises
        ------
        ValueError
            If has_math_latex is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("has_math_latex must be a bool")
        self._has_math_latex = bool(value)

    @property
    def code_lines(self):
        '''
        Returns the number of lines of code in the current code cell
        
        Raises
        ------
        ValueError
            If code_lines is not yet set
        '''
        if self._code_lines is None:
            raise ValueError("code_lines is not set")
        return self._code_lines

    @code_lines.setter
    def code_lines(self, value):
        '''
        Sets the number of lines that present codes in the cell 

        Raises
        ------
        ValueError
            If code_lines is not set in the integer type
        '''
        if not isinstance(value, int):
            raise ValueError("code_lines must be an int")
        self._code_lines = value

    @property
    def has_imports(self):
        '''
        Returns the status of whether or not the cell contains any imports
        '''
        return self._has_imports

    @has_imports.setter
    def has_imports(self, value):
        '''
        Sets the status of whether or not the cell contains any math latex

        Raises
        ------
        ValueError
            If has_imports is not set in the boolean type
        '''
        if not isinstance(value, bool):
            raise ValueError("has_imports must be a bool")
        self._has_imports = bool(value)

    @property
    def cell_execution_order(self):
        '''
        Returns the execution order number of the cell
        '''
        return self._cell_execution_order

    @cell_execution_order.setter
    def cell_execution_order(self, value):
        '''
        Sets the execution order number of the cell
        '''
        self._cell_execution_order = value

    @property
    def num_h1(self):
        '''
        Returns the number of the heading level 1 in the cell (H1)
        '''
        return self._num_h1

    @num_h1.setter
    def num_h1(self, value):
        '''
        Sets the number of the heading level 1 in the cell (H1)
        '''
        self._num_h1 = value

    @property
    def num_h2(self):
        '''
        Returns the number of the heading level 2 in the cell (H2)
        '''
        return self._num_h2

    @num_h2.setter
    def num_h2(self, value):
        '''
        Sets the number of the heading level 2 in the cell (H2)
        '''
        self._num_h2 = value

    @property
    def num_h3(self):
        '''
        Returns the number of the heading level 3 in the cell (H3)
        '''
        return self._num_h3

    @num_h3.setter
    def num_h3(self, value):
        '''
        Sets the number of the heading level 3 in the cell (H3)
        '''
        self._num_h3 = value

    @property
    def num_h4(self):
        '''
        Returns the number of the heading level 4 in the cell (H4)
        '''
        return self._num_h4

    @num_h4.setter
    def num_h4(self, value):
        '''
        Sets the number of the heading level 4 in the cell (H4)
        '''
        self._num_h4 = value

    @property
    def num_h5(self):
        '''
        Returns the number of the heading level 5 in the cell (H5)
        '''
        return self._num_h5

    @num_h5.setter
    def num_h5(self, value):
        '''
        Sets the number of the heading level 5 in the cell (H5)
        '''
        self._num_h5 = value

    @property
    def num_h6(self):
        '''
        Returns the number of the heading level 6 in the cell (H6)
        '''
        return self._num_h6

    @num_h6.setter
    def num_h6(self, value):
        '''
        Sets the number of the heading level 6 in the cell (H6)
        '''
        self._num_h6 = value

    @property
    def num_tables(self):
        '''
        Returns the number of tables presenting in the cell
        '''
        return self._num_tables

    @num_tables.setter
    def num_tables(self, value):
        '''
        Sets the number of tables in the cell
        '''
        return self._num_tables

    @property
    def table_metadata(self):
        '''
        Returns the table information in the cell
        '''
        return json.dumps(self._table_metadata)

    @table_metadata.setter
    def table_metadata(self, value):
        '''
        Sets the table information in the cell
        '''
        self._table_metadata = value

    @property
    def num_links(self):
        '''
        Returns the number of links in the cell
        '''
        return self._num_links

    @num_links.setter
    def num_links(self, value):
        '''
        Sets the number of links in the cell
        '''
        self._num_links = value
