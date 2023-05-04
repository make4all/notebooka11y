import string
from processors.import_processor import get_imports
import logging
import nbformat
import json
import pandas as pd
import numpy as np
import pandas as pd
import re

logging.basicConfig(filename="log/processNotebooks-100k-subplots.log", filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG

logger.setLevel(logging.DEBUG)
text = ''

DATA_DIRECTORY = 'data-100k/'
BASE64_IMG_DIRECTORY = 'base64Images/'
SAMPLE_DATA = 'sample-100000.csv'

def hasMatplotlib(line: "str"):
    if line.strip().startswith("#"):
        return False

    # fr matplotlib
    if '.subplots(' in line:
        return True
    
    return False


def hasBokeh(line: "str"):
    if line.strip().startswith("#"):
        return False

    # for bokeh
    if 'gridplot' in line:
        return True
    if 'column(' in line:
        return True
    if 'row(' in line:
        return True
    if 'layout(' in line:
        return True
    
    return False


def hasPlotly(line: "str"):
    if line.strip().startswith("#"):
        return False
    
    # for plotly
    if 'facet_' in line: 
        return True
    
    return False


def count_factory(check):
    def fn(row):
        filename = row['fileNames']
        data = row['raw']
        count = 0
        if data is None:
            return count
        cells = data['cells']
        for cell in cells:
            if cell['cell_type'] == 'code':
                src = cell['source']
                try:
                    for line in src.split('\n'):
                        if check(line):
                            count += 1
                except:
                    pass
            
        return count
    return fn

def getLanguage(x):
    """
    Takes each notebook and extracts the language information from the notebook.
    """
    language = None
    # x = row.raw
    if x is None:
        return None
    if 'metadata' not in x:
        return language
    if 'kernelspec' in x['metadata'].keys() and 'name' in x['metadata']['kernelspec']:
        language = x['metadata']['kernelspec']['name']
    elif 'language_info' in x['metadata'].keys():
        language = x['metadata']['language_info']['name']
    else:
        logger.exception("kernelspec and language_info keys not present in metadata. printing metadata entry for notebook")
        logger.error(x['metadata'])
        language = None
    return language


def getSourceCodeAndExtractImports(data_row):
    filename = data_row['fileNames']
    data = data_row['raw']
    import_strings = []
    if data is None:
        return json.dumps(import_strings)
    
    cells = data['cells']
    language = data_row['language']
    
    if language is not None and 'py' in language:
        for cell in cells:
            if cell['cell_type'] == 'code':
                src = cell['source']
                try:
                    import_list = get_imports(src)
                    for import_item in import_list:
                        modules = import_item.module
                        imported_names = import_item.name
                        import_str = ".".join(modules) + " " + ".".join(imported_names)
                        import_strings.append(import_str)
                except:
                    pass

    return json.dumps(import_strings)


def fileToNbNode(x):
    a = None
    try:
        # print("loading file: data-1k/" + x)
        a = nbformat.read(f"{DATA_DIRECTORY}{x}", as_version=4)
    except Exception as e:
        # print(x)
        logger.exception("Exception occurred for file '"+ x + "': "+ repr(e))
        
        a = None
    return a


# get base64 image metadata from each cell  
def storeBase64ImagesAndExtractImageMetadata(row):
    x = row['raw']
    image_metadata = []
    if x is None:
        return json.dumps(image_metadata)
    cells = x['cells']
    # base64Images = []
    
    for cell in cells:
        if cell['cell_type'] == 'code':
            # check if cell contains display type as images or plots
            if 'outputs' in cell.keys():
                outputs = cell['outputs']
                for output in outputs:
                    if 'data' in output.keys():
                        data = output['data']
                        keys = list(data.keys())
                        for k in keys:
                            image_metadata.append(k)
                        # if 'image/png' in data.keys():
                        #     # base64Images.append(data['image/png'])
                        #     image_metadata.append('png')
                        # elif 'image/jpeg' in data.keys():
                        #     # base64Images.append(data['image/jpeg'])
                        #     image_metadata.append('jpeg')
                        # elif 'image/svg+xml' in data.keys():
                        #     # base64Images.append(data['image/svg+xml'])
                        #     image_metadata.append('svg')
                            
    # Store the images into a directory
    # for i, image in enumerate(base64Images):
    #     image_file_name = f"{row['fileNames']}-{i}.png"
    #     try:
    #         with open(f"{DATA_DIRECTORY}{BASE64_IMG_DIRECTORY}{image_file_name}", "w") as f:
    #             f.write(image)
    #     except Exception as e:
    #         continue
    
    return json.dumps(image_metadata)


def get_code_markdown_cell_count(data):
    raw = data['raw']

    code_lines = []
    markdown_lines = []

    if raw is None:
        return json.dumps(code_lines), json.dumps(markdown_lines), sum(code_lines), sum(markdown_lines)
    
    cells = raw['cells']
    
    language = data['language']
    if language is not None and 'py' in language:
        for cell in cells:
            if cell['cell_type'] == 'code':
                src = cell['source']
                if src is None:
                    src = ""
                lines = src.split('\n')
                code_lines.append(len(lines))
            if cell['cell_type'] == 'markdown':
                src = cell['source']
                if src is None:
                    src = ""
                lines = None, src.split('\n')
                markdown_lines.append(len(lines))
    return json.dumps(code_lines), json.dumps(markdown_lines), sum(code_lines), sum(markdown_lines)



df = pd.read_csv('sample-100000.csv', names=['fileNames'])
validFiles = df.dropna()

results = []

for i, row in df.iterrows():
    filename = row['fileNames']
    if i % 1000 == 0:
        print(f'Processed {i}/{df.shape} records ...')
    raw = fileToNbNode(filename)
    language_info = getLanguage(raw)
    query_data = {'raw': raw, 'fileNames': filename, 'language': language_info}
    mpl_count = count_factory(hasMatplotlib)(query_data)
    plotly_count = count_factory(hasPlotly)(query_data)
    bokeh_count = count_factory(hasBokeh)(query_data)
    imports = getSourceCodeAndExtractImports(query_data)
    image_metadata = storeBase64ImagesAndExtractImageMetadata(query_data)
    num_images = len(json.loads(image_metadata))
    code_line_count, markdown_line_count, sum_code_lines, sum_markdown_lines = get_code_markdown_cell_count(query_data)

    results.append([
        filename,
        language_info,
        imports,
        num_images,
        image_metadata,
        mpl_count,
        plotly_count,
        bokeh_count,
        code_line_count,
        sum_code_lines,
        markdown_line_count,
        sum_markdown_lines
    ])

rdf = pd.DataFrame(data=results, columns=[
    'fileNames',
    'language',
    'imports',
    'num_images',
    'image_metadata',
    'has_matplotlib',
    'has_plotly',
    'has_bokeh',
    'code_lines',
    'total_code_lines',
    'markdown_lines',
    'sum_markdown_lines'
])

rdf.to_csv('submission-fixed-nb_processed.csv', header=True, index=False)



