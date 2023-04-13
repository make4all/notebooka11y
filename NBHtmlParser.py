# %% [markdown]
# # notebook to parse HTML exports of notebooks to get metadata
# please ensure that this, the CSV and the serve directory are pointed to correctly.
# ## imports
# %%
import json

from CellMetadata import NotebookCell
import pandas as pd
# from bs4 import BeautifulSoup
# from lxml import etree
from lxml import html
absolutePath = 'serve/light/'
# %% [markdown]
# ## lambdas
# %%
# get bs4 objects for each notebook and store them in the df


def supify(x):
    global absolutePath
    # replace .ipynb with .html
    fname = absolutePath + x.replace('.ipynb', '.html')

    soup = None
    try:
        soup = html.parse(fname).getroot()

    except Exception as e:
        # print(e)
        # print(fname)
        pass
    return soup

# get the number of h1, h2, h3, h4, h5 and h6


def getHeadings(tree):
    h1 = tree.xpath('count(.//h1)')
    h2 = tree.xpath('count(.//h2)')
    h3 = tree.xpath('count(.//h3)')
    h4 = tree.xpath('count(.//h4)')
    h5 = tree.xpath('count(.//h5)')
    h6 = tree.xpath('count(.//h6)')
    headingsDict = {'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4, 'h5': h5, 'h6': h6}
    return headingsDict

# get the cells from the notebook The following class structure for each cell: Classes (jp-Cell jp-CodeCell jp-Notebook-cell) give both the Input code cell and output code cell in a nesting under it


def getCellsFromRaw(row):
    # tree = raw
    raw = row['raw']

    notebookCells = []
    # find all cells that have jp-cell and jp-notebookcell and other classes
    cells = raw.cssselect('.jp-Cell.jp-Notebook-cell')
    # print(f"cells: {len(cells)}")
    # for each cell, make a NotebookCell object
    
    for cell in cells:
        cellClass = set(cell.classes)-set(['jp-Cell', 'jp-Notebook-cell'])
        # print(f"comparing cellClass: {cellClass} to jp-CodeCell and jp-mod-noOutputs")
        cellType = None
        # if class of cell is 'jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs' or 'jp-Cell jp-CodeCell jp-Notebook-cell', type is code
        if 'jp-mod-noOutputs' in cellClass or 'jp-CodeCell' in cellClass:
            # print("processing cell")
            cellType = 'code'
        if 'jp-MarkdownCell' in cellClass:
            cellType = 'markdown'
            # print(f"creating cellType: {cellType}")
            # print(f"class for cell {list(cell.classes)}")
        notebookCell = NotebookCell(row['fileNames'], cellType)
        if 'jp-mod-noOutputs' in cellClass or cellType == 'markdown':
            notebookCell.has_output= False
        headings = getHeadings(cell)
        # has_headings is true even if one value is > 0
        notebookCell.has_heading = any([headings['h1'] > 0, headings['h2'] > 0, headings['h3']
                                        > 0, headings['h4'] > 0, headings['h5'] > 0, headings['h6'] > 0])
        notebookCell.num_h1 = headings['h1']
        notebookCell.num_h2 = headings['h2']
        notebookCell.num_h3 = headings['h3']
        notebookCell.num_h4 = headings['h4']
        notebookCell.num_h5 = headings['h5']
        notebookCell.num_h6 = headings['h6']
        # has_links is true if any of the nodes has a link
        numLinks = cell.xpath('count(.//a)')
        notebookCell.has_links =  numLinks > 0
        notebookCell.num_links = numLinks
        # has_tables is true if the cell has tables.
        tables = cell.xpath('.//table')
        numTables = cell.xpath('count(.//table)')
        notebookCell.has_tables = numTables > 0
        tableMetadataList = []
        # print(f"processing {len(tables)} tables")
        for table in tables:
            # get the size of the table
            numRows = len(table.xpath('.//tr'))
            # get number of columns
            numColumns = len(table.xpath('.//td'))
            # get if table is uniform. todo.
            # isTableUniform = True
            # print(f"table is {numRows} x {numColumns}, and is uniform = {isTableUniform}. processing rows")
            # for row in table.xpath('.//tr'):
            #     if len(row[1].xpath('.//td')) != numColumns:
            #         print(f"table is not uniform. number of columns = {len(row.xpath('.//td'))}")
            #         print(f"markup is {html.tostring(row)}")
            #         isTableUniform = False
            #         break
            tableMetadata = {}
            tableMetadata['num_rows'] = numRows
            tableMetadata['num_columns'] = numColumns
            # tableMetadata['is_uniform'] = isTableUniform
            tableMetadataList.append(tableMetadata)
        notebookCell.num_tables = numTables
        notebookCell.table_metadata = json.dumps(tableMetadataList)
        numMath = len(cell.cssselect('.MathJax_Preview'))
        notebookCell.has_math = numMath > 0
        notebookCell.num_math = numMath
        # todo graphics and has_interactive

        notebookCells.append(vars(notebookCell))
        # print("appending")
        # print(dict(notebookCell))

    return notebookCells


# get a list of
# %%
# load the csv into a dataframe
processedDf = pd.read_csv('nb_subplots.csv')
# %%
# %% [markdown]
# # load the text file into a pandas dataframe
# %%
fnames = []
with open("sample-10000.txt") as f:
    for line in f:
        fnames.append(line.strip())
# load fnames into a pandas dataframe with column "fileNames"
print("Completed reading the data frame ...")
df = pd.DataFrame(fnames, columns=["fileNames"])
validFiles = df.dropna()
# %% [markdown]
# ## parse using lxml
# %%
validFiles['raw'] = validFiles['fileNames'].apply(lambda x: supify(x))
validFiles = validFiles.dropna()
print("valid files with lxml html nodes: ", validFiles.shape)
# print(validFiles.head())
# validFiles['headings'] = validFiles['raw'].apply(lambda x: getHeadings(x))
# %% [markdown]
# ## parse each cell.
# %%
validFiles['codeCellsWithOutput'] = validFiles.apply(
    lambda x: getCellsFromRaw(x), axis=1)

validFiles = validFiles.dropna()
print("valid files after getting cells ", validFiles.shape)
# %% [markdown]
# ## explode DF, drop, and save
# %% [markdown]
# ### add rows to validFiles.
# each row should contain one cell
# %%
validFiles = validFiles.drop(columns=['raw'])
validFiles = validFiles.explode('codeCellsWithOutput',True)
validFiles = validFiles.dropna()
print("validFiles after creating a cell for each row: ", validFiles.shape)
# print(validFiles.head())
# %% [markdown]
# #### expand NotebookCell objects
# %%
vf1 = validFiles.drop(['codeCellsWithOutput'], axis=1)
vf2 = validFiles['codeCellsWithOutput'].apply(pd.Series)
validFiles = pd.concat([vf1, vf2], axis=1)
print("validFiles after expanding noteBookCells ",validFiles.shape)
print(validFiles.head())
print(validFiles.describe())
# %% [markdown]
# #### save df to file
# %%
validFiles.to_csv('nb_processed_cell_html.csv',header=True, index=False)
