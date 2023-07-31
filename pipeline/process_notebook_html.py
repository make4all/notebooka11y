import glob
import json
import time

import pandas as pd
from lxml import html

from CellMetadata import NotebookCell

NOTEBOOKS_HTML_FORMAT = 'serve/light/'

CODE_CELL_CLASSES = ['jp-Cell', 'jp-Notebook-cell']
CELL_SELECTOR = '.jp-Cell.jp-Notebook-cell'

CELL_HTML_DATASET = 'data_out/nb_processed_cell_html.csv'


def supify(fname):
    '''
    Returns the cells of the notebook in the given html notebook file  #TODO: does this sound right?

    Parameters
    ----------
        fname : str
            The path of the file to be processed
    '''
    soup = None
    try:
        soup = html.parse(fname).getroot()
    except Exception as e:
        pass
    return get_cells_from_raw(fname, soup)


def get_headings(tree):
    '''
    Returns the heading counts and texts present in the given html tree    #TODO: does this sound right?

    Parameters
    ----------
        tree : html.HtmlElement
            The tree to be processed
    '''
    h1 = tree.xpath('count(.//h1)')
    h2 = tree.xpath('count(.//h2)')
    h3 = tree.xpath('count(.//h3)')
    h4 = tree.xpath('count(.//h4)')
    h5 = tree.xpath('count(.//h5)')
    h6 = tree.xpath('count(.//h6)')

    h1_texts = tree.xpath('.//h1/text()')
    h2_texts = tree.xpath('.//h2/text()')
    h3_texts = tree.xpath('.//h3/text()')
    h4_texts = tree.xpath('.//h4/text()')
    h5_texts = tree.xpath('.//h5/text()')
    h6_texts = tree.xpath('.//h6/text()')
    headings_dict = {
        'h1': h1,
        'h2': h2,
        'h3': h3,
        'h4': h4,
        'h5': h5,
        'h6': h6,
        'h1-texts': json.dumps(h1_texts),
        'h2-texts': json.dumps(h2_texts),
        'h3-texts': json.dumps(h3_texts),
        'h4-texts': json.dumps(h4_texts),
        'h5-texts': json.dumps(h5_texts),
        'h6-texts': json.dumps(h6_texts)
    }
    return headings_dict


def get_cells_from_raw(fname, raw):
    '''
    Analyzes the given raw html and returns the metadata of the cells in the notebook
    as a list of NotebookCell objects.

    Parameters
    ----------
        fname : str
            The path of the file to be processed
        raw : html.HtmlElement | None
            The raw html to be processed
    '''
    if raw is None:
        return None

    notebook_cells = []
    cells = raw.cssselect(CELL_SELECTOR)

    for cell in cells:
        cell_class = set(cell.classes) - set(CODE_CELL_CLASSES)
        cell_type = None

        if 'jp-mod-noOutputs' in cell_class or 'jp-CodeCell' in cell_class:
            cell_type = 'code'
            num_code_lines = cell.xpath('count(.//span)') - 1
        if 'jp-MarkdownCell' in cell_class:
            cell_type = 'markdown'
        notebook_cell = NotebookCell(fname, cell_type)
        if cell_type == 'code':
            if 'jp-mod-noOutputs' in cell_class:
                notebook_cell.has_output = False
            else:
                notebook_cell.has_output = True
            notebook_cell.code_lines = int(num_code_lines)

        if 'jp-mod-noOutputs' in cell_class or cell_type == 'markdown':
            notebook_cell.has_output = False
        headings = get_headings(cell)
        # has_headings is true even if one value is > 0
        notebook_cell.has_heading = any([headings['h1'] > 0,
                                         headings['h2'] > 0,
                                         headings['h3'] > 0,
                                         headings['h4'] > 0,
                                         headings['h5'] > 0,
                                         headings['h6'] > 0])
        notebook_cell.num_h1 = headings['h1']
        notebook_cell.num_h2 = headings['h2']
        notebook_cell.num_h3 = headings['h3']
        notebook_cell.num_h4 = headings['h4']
        notebook_cell.num_h5 = headings['h5']
        notebook_cell.num_h6 = headings['h6']
        # Get heading texts
        notebook_cell.h1_texts = headings['h1-texts']
        notebook_cell.h2_texts = headings['h2-texts']
        notebook_cell.h3_texts = headings['h3-texts']
        notebook_cell.h4_texts = headings['h4-texts']
        notebook_cell.h5_texts = headings['h5-texts']
        notebook_cell.h6_texts = headings['h6-texts']
        # has_links is true if any of the nodes has a link
        num_links = cell.xpath('count(.//a)')
        notebook_cell.has_links = num_links > 0
        notebook_cell.num_links = num_links
        # has_tables is true if the cell has tables.
        tables = cell.xpath('.//table')
        num_tables = cell.xpath('count(.//table)')
        notebook_cell.has_tables = num_tables > 0
        table_metadata_list = []

        for table in tables:
            # get the size of the table
            num_rows = len(table.xpath('.//tr'))
            # get number of columns
            num_columns = len(table.xpath('.//td'))
            table_metadata = {
                'num_rows': num_rows,
                'num_columns': num_columns
            }
            table_metadata_list.append(table_metadata)
        notebook_cell.num_tables = num_tables
        notebook_cell.table_metadata = json.dumps(table_metadata_list)
        num_math = len(cell.cssselect('.MathJax_Preview'))
        num_rendered_image = len(cell.cssselect('.jp-RenderedImage.jp-OutputArea-output'))
        notebook_cell.has_math = num_math > 0
        notebook_cell.num_math = num_math
        notebook_cell.output_contains_graphics = num_rendered_image > 0
        # look for img elements and their alt texts
        alts = cell.xpath('.//img/@alt')
        notebook_cell.alt_text = json.dumps(alts)

        notebook_cells.append(vars(notebook_cell))

    return notebook_cells


fnames = glob.glob(f'{NOTEBOOKS_HTML_FORMAT}/*.html')
df = pd.DataFrame(fnames, columns=['fileNames'])
print(f"Shape of df is {df.shape}")

valid_files = df.dropna()

start_time = time.time()

# Parse using lxml
valid_files['cells'] = valid_files['fileNames'].apply(lambda x: supify(x))
valid_files = valid_files.dropna()
print("Valid files with lxml html nodes: ", valid_files.shape)

valid_files = valid_files.explode('cells', True)
valid_files = valid_files.dropna()
print("validFiles after creating a cell for each row: ", valid_files.shape)

vf1 = valid_files.drop(['cells'], axis=1)
vf2 = valid_files['cells'].apply(pd.Series)
valid_files = pd.concat([vf1, vf2], axis=1)
print("validFiles after expanding noteBookCells ", valid_files.shape)
print(valid_files.head())
print(valid_files.describe())

end_time = time.time()

print(f'Time taken to process HTML into dataset: {end_time - start_time} seconds')

valid_files.to_csv(CELL_HTML_DATASET, header=True, index=False)
