import ast
from collections import namedtuple

Import = namedtuple("Import", ["module", "name", "alias"])

replacements = ['%matplotlib inline', '%pylab inline', '']

def get_imports(code):
    code_lines = code.split('\n')
    corrected_code = []
    for code_line in code_lines:
        temp = code_line
        code_line = code_line.lstrip()
        if len(code_line) == 0:
            continue
        if code_line[0] in ['!', '?', '%']:
            continue
        if code_line[-1] == '?':
            continue
        corrected_code.append(temp)
    
    code = "\n".join(corrected_code)

    for replacement in replacements:
        code = code.replace(replacement, "")

    root = ast.parse(code)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue
        
        for n in node.names:
            yield Import(module=module, name=n.name.split('.'), alias=n.asname)
