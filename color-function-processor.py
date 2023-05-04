# %% [markdown]
# # Look for popular ways of people using color functions
# %% [markdown]
# ## imports and setup
# %%
from processors.import_processor import get_imports
from processors.call_processors import CallProcessor
import logging
import nbformat
import json
import pandas as pd
import re
import swifter
import ast
from collections import namedtuple
BASE_DATA_DIR = 'data-100k/'


def loadProcessedNotebooksdf(filename='nb_processed.csv'):
    df = pd.read_csv(filename)
    print(f"loaded csv file{filename} of {df.shape} ")
    return df

# %% [markdown]
# ## lambdas and other helper functions


def fileToNbNode(x):
    a = None
    try:
        # print("loading file: data-1k/" + x)
        a = nbformat.read(f'{BASE_DATA_DIR}' + x, as_version=4)
    except Exception as e:
        print(x)
        # logger.exception("Exception occurred for file '"+ x + "': "+ repr(e))

        a = None
    return a


def correctCodeLines(codeLines):
    replacements = ['%matplotlib inline', '%pylab inline', '']
    correctedCodeLines = []
    for codeLine in codeLines:
        temp = codeLine
        codeLine = codeLine.lstrip()
        if len(codeLine) == 0:
            continue
        if codeLine[0] in ['!', '?', '%', '#']:
            continue
        if codeLine[-1] == '?':
            continue
        correctedCodeLines.append(temp)
    code = "\n".join(correctedCodeLines)
    # replace occurances of replacements with empty
    for replacement in replacements:
        code = code.replace(replacement, "")
    return code.splitlines()


def removeAliasCodeLines(importAliasMapping, codeLines):
    correctedCodeLines = []
    for codeLine in codeLines:
        for module, alias in importAliasMapping.items():
            if alias in codeLine:
                codeLine = codeLine.replace(alias, module)
        correctedCodeLines.append(codeLine)
    return correctedCodeLines


def getMatplotLibColorFunctionUsage(filename):
    notebook = fileToNbNode(filename)
    linesOfCode = 0
    # check if cell is of type source and append it to a list called sourceCells
    sourceCells = []
    functionCalls = []
    importAliasMapping = {}
    functionCall = namedtuple('functionName',  'arguments')

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            sourceCells.append(cell)
    # print(code)
    # import_list = []
    import_strings = []
    alias_strings = []
    for sourceCell in sourceCells:
        try:
            import_list = get_imports(sourceCell['source'])
            # print(f" import list : {import_list}")
            # check if imports has matplotlib and if there are any aliases
            # if there are aliases, then we need to check if they are used in the code when calling color
            for importItem in import_list:
                modules = importItem.module
                name = importItem.name
                alias = importItem.alias
                import_string = ".".join(modules) + \
                    " " + ".".join(name)  # + " as "+alias
                # print alias if it is not none
                if alias is not None:
                    # print(f" alias is {alias}")
                    import_string = import_string + " as "+alias

                if "matplotlib" in import_string:
                    import_strings.append(import_string)
        except:
            pass
    # print(f"import strings: {import_strings}")

    # print(f"import_strings is {import_strings}")
    # construct a dictionary of module import and alias
    for import_string in import_strings:
        import_string = import_string.split("as")
        # print(f" split import_string is {import_string}")
        module = import_string[0] if len(import_string) > 0 else None
        alias = import_string[1] if len(import_string) > 1 else None
        if alias is not None:
            # strip spaces from module and alias
            module = module.strip()
            alias = alias.strip()
            importAliasMapping[module] = alias
    # print(f"importAliasMapping is {importAliasMapping}")
    for sourceCell in sourceCells:
        codeLines = sourceCell['source'].splitlines()
        in_c = codeLines
        codeLines = correctCodeLines(codeLines)
        cc_c = codeLines
        # codeLines = removeAliasCodeLines(importAliasMapping, codeLines)
        # rc_c = codeLines
        # pltColorFunctions = ['colors','colorbar']
        # using ast, check if a codeline is a function call

        # print(f"code lines before checking for function calls is of length: {len(codeLines)} ")
        linesOfCode += len(codeLines)
        codeLines = "\n".join(codeLines)
        try:
            root = ast.parse(codeLines)
            cc = CallProcessor()
            cc.visit(root)
            functionList = cc.calls
            # print(f"root is {root}")
            # for node in ast.walk(root):
                # print("in iter_child loop")
            #     if isinstance(node, ast.Call):
            #         print(f" instance of ast.Call is {node}")
                    # get the name of the function
            #         if type(node) in m:
            #             m[type(node.func)] = m[type(node.func)] + 1
            #         else:
            #             m[type(node.func)] = 1
            #         if isinstance(node.func, ast.Attribute):
            #             functionName = node.func.value
            #             arguments = node.func.attr
            #         if isinstance(node.func, ast.Name):
            #             functionName = node.func.id
            #             arguments = node.func.args
            #         print(f"function name: {functionName}, arguments: {arguments}")
                    # check if the function call is of matplotlib
            for f in functionList:
                functionCalls.append(f)
            #         if functionName.contains("matplotlib"):
            #             functionCalls.append(
            #                     functionCall(
            #                         functionName=functionName,
            #                         arguments=arguments)
            #                     )
        except Exception as e:
            print(f'Exception : {e} {codeLines[:10]}')
            pass


    return json.dumps(functionCalls), linesOfCode


# %% [markdown]
# ## entry point
# %%
df = loadProcessedNotebooksdf()
df['functionCalls'], df['linesOfCode'] = zip(*df.swifter.apply(lambda x: getMatplotLibColorFunctionUsage(x['fileNames']), axis=1))
print(df.head(5))
df.to_csv('processed_function_calls.csv', header=True, index=False)

