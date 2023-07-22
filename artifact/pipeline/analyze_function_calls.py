import ast
import json
import time

import nbformat
import pandas as pd

from processors.import_processor import get_imports
from processors.call_processors import CallProcessor


BASE_DATA_DIR = 'data-100k/'
JUPYTER_MAGICS = ['%matplotlib inline', '%pylab inline', '']
JUPYTER_MAGIC_STARTERS = ['!', '?', '%', '#']
JUPYTER_HELP_DOCUMENTATION_COMMAND = '?'


NOTEBOOKS_WITH_FIGURE_OUTPUTS = 'nb_processed.csv'
FUNCTION_CALL_RESULTS = 'data_out/processed_function_calls.csv'


def load_processed_notebooksdf(filename=NOTEBOOKS_WITH_FIGURE_OUTPUTS):
    df = pd.read_csv(filename)
    return df


def file_to_nb_node(x):
    a = None
    try:
        a = nbformat.read(f'{BASE_DATA_DIR}' + x, as_version=4)
    except Exception as e:
        a = None
    return a


def correct_code_lines(code_lines):
    replacements = JUPYTER_MAGICS
    corrected_code_lines = []
    for code_line in code_lines:
        temp = code_line
        code_line = code_line.lstrip()
        if len(code_line) == 0:
            continue
        if code_line[0] in JUPYTER_MAGIC_STARTERS:
            continue
        if code_line[-1] == JUPYTER_HELP_DOCUMENTATION_COMMAND:
            continue
        corrected_code_lines.append(temp)
    code = "\n".join(corrected_code_lines)

    for replacement in replacements:
        code = code.replace(replacement, "")
    return code.splitlines()


def remove_alias_code_lines(import_alias_mapping, code_lines):
    corrected_code_lines = []
    for code_line in code_lines:
        for module, alias in import_alias_mapping.items():
            if alias in code_line:
                code_line = code_line.replace(alias, module)
        corrected_code_lines.append(code_line)
    return corrected_code_lines


def get_function_usage(filename):
    notebook = file_to_nb_node(filename)
    lines_of_code = 0
    # check if cell is of type source and append it to a list called sourceCells
    source_cells = []
    function_calls = []
    import_alias_mapping = {}

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source_cells.append(cell)

    import_strings = []

    for source_cell in source_cells:
        try:
            import_list = get_imports(source_cell['source'])
            for importItem in import_list:
                modules = importItem.module
                name = importItem.name
                alias = importItem.alias
                import_string = ".".join(modules) + \
                    " " + ".".join(name)  # + " as "+alias
                # print alias if it is not none
                if alias is not None:
                    import_string = import_string + " as "+alias

                if "matplotlib" in import_string:
                    import_strings.append(import_string)
        except:
            pass

    for import_string in import_strings:
        import_string = import_string.split("as")
        module = import_string[0] if len(import_string) > 0 else None
        alias = import_string[1] if len(import_string) > 1 else None
        if alias is not None:
            # strip spaces from module and alias
            module = module.strip()
            alias = alias.strip()
            import_alias_mapping[module] = alias

    for source_cell in source_cells:
        code_lines = source_cell['source'].splitlines()
        code_lines = correct_code_lines(code_lines)

        lines_of_code += len(code_lines)
        code_lines = "\n".join(code_lines)
        try:
            root = ast.parse(code_lines)
            cc = CallProcessor()
            cc.visit(root)
            function_list = cc.calls
            for f in function_list:
                function_calls.append(f)
        except Exception as e:
            pass

    return json.dumps(function_calls), lines_of_code


df = load_processed_notebooksdf()

start_time = time.time()
df['functionCalls'], df['linesOfCode'] = zip(*df.apply(lambda x: get_function_usage(x['fileNames']), axis=1))
end_time = time.time()

print(f'Time taken to create the function calls result: {end_time - start_time} seconds')
df.to_csv(FUNCTION_CALL_RESULTS, header=True, index=False)
