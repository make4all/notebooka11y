# %% [markdown]
# # notebook to parse HTML exports of notebooks to get metadata
# please ensure that this, the CSV and the serve directory are pointed to correctly.
# ## imports
# %%

from os import access
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
    h1 = tree.xpath('//h1')
    h2 = tree.xpath('//h2')
    h3 = tree.xpath('//h3')
    h4 = tree.xpath('//h4')
    h5 = tree.xpath('//h5')
    h6 = tree.xpath('//h6')
    headingsDict = {'h1': len(h1), 'h2': len(h2), 'h3': len(
        h3), 'h4': len(h4), 'h5': len(h5), 'h6': len(h6)}
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
        headings = getHeadings(cell)
        # has_headings is true even if one value is > 0
        notebookCell.has_heading = any([headings['h1'] > 0, headings['h2'] > 0, headings['h3']
                                        > 0, headings['h4'] > 0, headings['h5'] > 0, headings['h6'] > 0])
        # has_links is true if any of the nodes has a link
        notebookCell.has_links = len(cell.xpath('.//a')) > 0
        # has_tables is true if the cell has tables.
        notebookCell.has_tables = len(cell.xpath('.//table')) > 0
        notebookCells.append(vars(notebookCell))
        # print("appending")
        # print(dict(notebookCell))

    return notebookCells


# get a list of
# %%
# load the csv into a dataframe
processedDf = pd.read_csv('nb_processed.csv')
# %%
# %% [markdown]
# # load the text file into a pandas dataframe
# %%
fnames = []
with open("data-1k/sample-1000.txt") as f:
    for line in f:
        fnames.append(line.strip())
# load fnames into a pandas dataframe with column "fileNames"
df = pd.DataFrame(fnames, columns=["fileNames"])
validFiles = df.dropna()
print(f"loaded {validFiles.shape}")
validFiles['raw'] = validFiles['fileNames'].apply(lambda x: supify(x))
validFiles = validFiles.dropna()
print("valid files with lxml html nodes: ", validFiles.shape)
# print(validFiles.head())
# validFiles['headings'] = validFiles['raw'].apply(lambda x: getHeadings(x))
validFiles['codeCellsWithOutput'] = validFiles.apply(
    lambda x: getCellsFromRaw(x), axis=1)

validFiles = validFiles.dropna()
print("valid files after getting cells ", validFiles.shape)
# %% [markdown]
# # explode DF, drop, and save
# %%
# add rows to validFiles. each row should contain one cell
validFiles = validFiles.drop(columns=['raw'])
validFiles = validFiles.explode('codeCellsWithOutput')
validFiles = validFiles.dropna()
print("validFiles after creating a cell for each row: ", validFiles.shape)
print(validFiles.head())
