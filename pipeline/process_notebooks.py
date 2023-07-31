from processors.import_processor import get_imports

import json
import nbformat
import os
import pandas
import time


BASE_DATA_DIR = 'data-100k/'
OUTPUT_IMAGE_DIRECTORY = f'{BASE_DATA_DIR}base64Images/'
NB_FILE_LIST = 'pipeline/input_data/100k-dataset.csv'

OUTPUT_DATASET = 'data_out/nb_processed.csv'

os.makedirs(OUTPUT_IMAGE_DIRECTORY, exist_ok=True)


def file_to_nb_node(filename):
    '''
    Returns the notebook data from the given file in the given Jupiter notebook format

    Parameters
    ----------
        filename : str | None
            The path of the file to be processed
    '''
    f = None
    try:
        f = nbformat.read(f"{BASE_DATA_DIR}{filename}", as_version=4)
    except Exception as e:
        f = None
    return f


def get_language(nb_data):
    '''
    Returns the language of the given notebook data    #TODO: specify what language means here? 

    Parameters
    ----------
        nb_data : dict | None
            The notebook data to be processed
    '''
    language = None
    if nb_data is None:
        return language
    if 'metadata' not in nb_data:
        return language
    if 'kernelspec' in nb_data['metadata'].keys() and 'name' in nb_data['metadata']['kernelspec']:
        language = nb_data['metadata']['kernelspec']['name']
    elif 'language_info' in nb_data['metadata'].keys():
        language = nb_data['metadata']['language_info']['name']
    else:
        language = None
    return language


def has_matplotlib(line: "str"):
    '''
    Returns whether the given line contains a matplotlib subplot (small multiples)  function call

    Parameters
    ----------
        line : str
            The line to be processed
    '''
    if line.strip().startswith("#"):
        return False

    if '.subplots(' in line:
        return True
    return False


def has_bokeh(line: "str"):
    '''
    Returns whether the given line contains a bokeh subplot function call

    Parameters
    ----------
        line : str
            The line to be processed
    '''
    if line.strip().startswith("#"):
        return False
    if 'gridplot' in line:
        return True
    if 'column(' in line:
        return True
    if 'row(' in line:
        return True
    if 'layout(' in line:
        return True
    return False


def has_plotly(line: "str"):
    '''
    Returns whether the given line contains a plotly subplot (small multiples) function call

    Parameters
    ----------
        line : str
            The line to be processed
    '''
    if line.strip().startswith("#"):
        return False
    if 'facet_' in line:
        return True
    return False


def count_factory(check):
    '''
    Returns a function that counts the number of lines in the given source that satisfy the given check function

    Parameters
    ----------
        check : function
            The function to be used to check the lines
    '''
    def fn(src):
        count = 0
        try:
            for line in src.split('\n'):
                if check(line):
                    count += 1
        except:
            pass
        return count
    return fn


def process_notebooks(row):
    '''
    Analyzes the input notebook and returns the counts of the various 
    features of the notebook in the given format

    Parameters
    ----------
        row : pandas.Series
            The row of the dataframe to be processed
    '''
    result = {}

    filename = row['fileNames']
    nb_data = file_to_nb_node(filename)

    language = get_language(nb_data)

    code_lines = []
    markdown_lines = []

    import_strings = []
    output_metadata = []

    base64_images = []

    matplotlib_count = 0
    bokeh_count = 0
    plotly_count = 0

    if language is not None and 'py' in language:
        cells = nb_data['cells']
        for cell in cells:
            if cell['cell_type'] == 'code':
                src = cell['source']
                if src is None:
                    src = ""
                lines = src.split('\n')
                code_lines.append(len(lines))

                matplotlib_count += count_factory(has_matplotlib)(src)
                plotly_count += count_factory(has_plotly)(src)
                bokeh_count += count_factory(has_bokeh)(src)

                if 'outputs' in cell.keys():
                    outputs = cell['outputs']
                    for output in outputs:
                        if 'data' in output.keys():
                            data = output['data']
                            keys = list(data.keys())
                            for k in keys:
                                output_metadata.append(k)
                                if k in ['image/png', 'image/jpeg', 'image/svg+xml']:
                                    ext = 'png'
                                    if 'jpeg' in k:
                                        ext = 'jpeg'
                                    if 'svg' in k:
                                        ext = 'svg'
                                    base64_images.append((data[k], ext))

                try:
                    import_list = get_imports(src)
                    for import_item in import_list:
                        modules = import_item.module
                        imported_names = import_item.name
                        import_str = ".".join(modules) + " " + ".".join(imported_names)
                        import_strings.append(import_str)
                except:
                    pass

            if cell['cell_type'] == 'markdown':
                src = cell['source']
                if src is None:
                    src = ""
                lines = src.split('\n')
                markdown_lines.append(len(lines))

    # Store any images to a directory
    for i, image_and_ext in enumerate(base64_images):
        image, ext = image_and_ext
        img_file_name = f'{filename}-{i}.{ext}'
        try:
            with open(f"{OUTPUT_IMAGE_DIRECTORY}{img_file_name}", "w") as f:
                f.write(image)
        except Exception as e:
            continue

    image_metadata = [i for i in output_metadata if i in ['image/png', 'image/jpeg', 'image/svg+xml']]

    result['filename'] = filename
    result['language'] = language
    result['imports'] = json.dumps(import_strings)
    result['num_images'] = len(image_metadata)
    result['output_metadata'] = json.dumps(output_metadata)
    result['image_metadata'] = json.dumps(image_metadata)
    result['matplotlib_count'] = matplotlib_count
    result['plotly_count'] = plotly_count
    result['bokeh_count'] = bokeh_count
    result['code_line_count'] = json.dumps(code_lines)
    result['sum_code_lines'] = sum(code_lines)
    result['markdown_line_count'] = json.dumps(markdown_lines)
    result['sum_markdown_lines'] = sum(markdown_lines)
    return result


def main():
    df = pandas.read_csv(NB_FILE_LIST, names=['fileNames'])

    columns = ['fileNames', 'language', 'imports', 'num_images', 'output_metadata', 'image_metadata', 'has_matplotlib',
               'has_plotly', 'has_bokeh', 'code_lines', 'total_code_lines', 'markdown_lines', 'sum_markdown_lines']
    results = []

    for i, row in df.iterrows():
        res = process_notebooks(row)
        results.append([
            res['filename'],
            res['language'],
            res['imports'],
            res['num_images'],
            res['output_metadata'],
            res['image_metadata'],
            res['matplotlib_count'],
            res['plotly_count'],
            res['bokeh_count'],
            res['code_line_count'],
            res['sum_code_lines'],
            res['markdown_line_count'],
            res['sum_markdown_lines']
        ])

    rdf = pandas.DataFrame(data=results, columns=columns)
    rdf.to_csv(OUTPUT_DATASET, header=True, index=False)


start_time = time.time()
main()
end_time = time.time()
print(f'Time taken: {end_time - start_time} seconds')

