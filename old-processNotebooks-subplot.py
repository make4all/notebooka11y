# from cmath import nan
# from logging import exception
# from tkinter import E
# from tkinter import E
# %%
import string
from processors.import_processor import get_imports
import logging
import nbformat
import json
import pandas as pd
import numpy as np
import pandas as pd
import pypandoc
import re
# import pyspark
# from pyspark.sql import *
# from pyspark.sql.functions import *
# from pyspark import SparkContext, SparkConf
# Create and configure logger
logging.basicConfig(filename="log/processNotebooks.log", filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG

logger.setLevel(logging.DEBUG)
text = ''
# initialize spark
# Let's initialize the Spark context.
# create the session
# conf = SparkConf().set("spark.ui.port", "4050")

# # create the context
# sc = pyspark.SparkContext(conf=conf)
# spark = SparkSession.builder.getOrCreate()
# %% [markdown]
# # lambdas
# %%
def getLanguage(x):
    language = None
    # x = row.raw
    if 'kernelspec' in x['metadata'].keys() :
        language = x['metadata']['kernelspec']['name']
    elif 'language_info' in x['metadata'].keys():
        language = x['metadata']['language_info']['name']
    else:
        logger.exception("kernelspec and language_info keys not present in metadata. printing metadata entry for notebook")
        logger.error(x['metadata'])
        language = None
    return language    
# get code cells with images and plots
def getSourceFromCells(x):
    cells = x['cells']
    codeCells = []
    for cell in cells:
        if cell['cell_type'] == 'code':
            # check if cell contains display type as images or plots
            if 'outputs' in cell.keys():
                outputs = cell['outputs']
                for output in outputs:
                    if 'data' in output.keys():
                        data = output['data']
                        if 'image/png' in data.keys():
                            codeCells.append(cell['source'])
                        elif 'image/jpeg' in data.keys():
                            codeCells.append(cell['source'])
                        elif 'image/svg+xml' in data.keys():
                            codeCells.append(cell['source'])

            #codeCells.append(cell)
    
    if len(codeCells) == 0:
        codeCells = None
    return codeCells

def getSourceCodeAndExtractImports(data_row):
    filename = data_row['fileNames']
    data = data_row['raw']
    cells = data['cells']
    import_strings = []
    print(f'Processing {filename}')
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


def subplotLibrary(line: "str"):
    if line.strip().startswith("#"):
        return False

    # fr matplotlib
    if '.subplot(' in line:
        return 'matplotlib'

    # for bokeh
    if 'gridplot' in line:
        return 'bokeh' 
    if 'column(' in line:
        return 'bokeh' 
    if 'row(' in line:
        return 'bokeh' 
    if 'layout(' in line:
        return 'bokeh' 
    
    # for plotly
    if 'facet_' in line: 
        return 'plotly' 
    
    return False


def getSourceCodeAndExtractSubplotCount(data_row):
    filename = data_row['fileNames']
    data = data_row['raw']
    cells = data['cells']
    subplots = []
    subplot_count = {}
    print(f'Processing {filename}')
    for cell in cells:
        if cell['cell_type'] == 'code':
            src = cell['source']
            try:
                for line in src.split('\n'):
                    subplotlibrary = subplotLibrary(line)
                    if not subplotlibrary:
                        continue
                    if subplotlibrary not in subplot_count:
                        subplot_count[subplotlibrary] = 0
                    subplot_count[subplotlibrary] += 1
            except:
                pass

    return subplot_count


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
        cells = data['cells']
        count = 0
        print(f'Processing {filename}')
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


# get output cells
def getOutputFromCells(x):
    cells = x['cells']
    outputCells = []
    for cell in cells:
        if cell['cell_type'] == 'code':
            # check if cell contains display type as images or plots
            if 'outputs' in cell.keys():
                outputs = cell['outputs']
                for output in outputs:
                    if 'data' in output.keys():
                        data = output['data']
                        if 'image/png' in data.keys():
                            outputCells.append(output)
                        elif 'image/jpeg' in data.keys():
                            outputCells.append(output)
                        elif 'image/svg+xml' in data.keys():
                            outputCells.append(output)

            #codeCells.append(cell)
    if(len(outputCells) == 0):
        outputCells = None
    return outputCells

# get base64 image metadata from each cell  
def getBase64FromCells(x):
    cells = x['cells']
    base64Images = []
    for cell in cells:
        if cell['cell_type'] == 'code':
            # check if cell contains display type as images or plots
            if 'outputs' in cell.keys():
                outputs = cell['outputs']
                for output in outputs:
                    if 'data' in output.keys():
                        data = output['data']
                        if 'image/png' in data.keys():
                            base64Images.append(data['image/png'])
                        elif 'image/jpeg' in data.keys():
                            base64Images.append(data['image/jpeg'])
                        elif 'image/svg+xml' in data.keys():
                            base64Images.append(data['image/svg+xml'])

            #codeCells.append(cell)
    
    if len(base64Images) == 0:
        base64Images = None
    return base64Images

def fileToNbNode(x):
    a = None
    try:
        # print("loading file: data-1k/" + x)
        a = nbformat.read("data-1k/" + x, as_version=4)
    except Exception as e:
        # print(x)
        logger.exception("Exception occurred for file '"+ x + "': "+ repr(e))
        
        a = None
    return a
# store the base 64 images into a file
def storeBase64(row):
    i=0
    for image in row['images']:
        imageFileName = row['fileNames'] + "-"+str(i)+".png" 
        try:
            with open("data-1k/base64Images/"+imageFileName, "w") as f:
                f.write(image)
        except Exception as     e:
            logger.exception("Exception occurred for file '"+ imageFileName + "': "+ repr(e))
        i = i+1

# get text from the raw column and store it in a new column 'text'.
def getTextFromCells(raw):
    text = ''
    for cell in raw['cells']:
        if cell['cell_type'] == 'markdown':
            text += cell['source']
    if len(text) > 0:
        try:
            plain = pypandoc.convert_text(text, 'plain', format='md', extra_args=['--wrap=none'])
        except Exception as e:
            logger.exception("Exception occurred for string '"+ text + "': "+ repr(e))
            plain = None
        return plain
    else:
        return None


def getPlainText(textColumn):
    global text
    text = text+textColumn


# %% [markdown]
# ## load the text file into a pandas dataframe
# %%
fnames = []
with open("data-1k/sample-1000.txt") as f:
    for line in f:
        fnames.append(line.strip())
# load fnames into a pandas dataframe with column "fileNames"
df = pd.DataFrame(fnames, columns=["fileNames"])
validFiles = df.dropna()
# print("number of valid files")

# fnames = pd.read_csv("data-1k/sample-1000.txt", sep="\n", header=None, names=["fileNames"])

# print the dataframe
# prevent truncation when printing

# for each fileName in df, load it using nbformat and store it in a new column "raw"
df['raw'] = df['fileNames'].apply(lambda x: fileToNbNode(x))
validFiles = df.dropna()
print("number of valid files")
print(validFiles.count())
# validFiles.set_option('display.width', 999)
pd.options.display.max_colwidth = 999
# print(validFiles.count())
# %% [markdown]
# ## now get the kernel type and language for each file and store it in the "language" column of this dataframe.
# %%
validFiles['language'] = validFiles['raw'].apply(lambda x: getLanguage(x) )
print(f'Shape of validfiles with language: {validFiles.shape}')
# logger.info(validFiles[['fileNames','language']].head(20))
validFiles= validFiles.dropna()
print(f'Validfiles with drop na after language : {validFiles.shape}')
# %% [markdown]
# ## check if file is python.
# %%
validFiles = validFiles[validFiles['language'].str.contains('py')]
print(f'Validfiles with language filter: {validFiles.shape}')
# %% [markdown]
# ## Get the subplot information
# %%

# validFiles['subplot_count'] = validFiles.apply(lambda nb: getSourceCodeAndExtractSubplotCount(nb), axis=1)
validFiles['matplotlib_count'] = validFiles.apply(lambda nb: count_factory(hasMatplotlib)(nb), axis=1)
validFiles['plotly_count'] = validFiles.apply(lambda nb: count_factory(hasPlotly)(nb), axis=1)
validFiles['bokeh_count'] = validFiles.apply(lambda nb: count_factory(hasBokeh)(nb), axis=1)
print(validFiles.head(50))
# %% [markdown]
## drop files that are not python
# %%
validFiles['imports'] = validFiles.apply(lambda nb: getSourceCodeAndExtractImports(nb), axis=1)
# languageGroups = validFiles.groupby('language').count()
# logger.info(languageGroups.head(10))
logger.info(" number of files after dropping values with no language_info is")
logger.info(validFiles.count())

validFiles['source'] = validFiles['raw'].apply(lambda x: getSourceFromCells(x))
validFiles['output'] = validFiles['raw'].apply(lambda x: getOutputFromCells(x))
validFiles= validFiles.dropna()
logger.info("valid files with code cells with outputs")
logger.info(validFiles.count())
validFiles['images'] = validFiles['raw'].apply(lambda x: getBase64FromCells(x))
validFiles = validFiles.dropna()
logger.info("valid files with base64 image outputs")
logger.info(validFiles.count())
validFiles['numImages'] = validFiles['images'].apply(lambda x: len(x))
logger.info("sum of numImages column")
logger.info(validFiles['numImages'].sum())

logger.info(validFiles[['fileNames','language','numImages']].head(5))
# %% [markdown]
# ## convert each of these base64 images into pngs and store them on disc.
# uncomment code below
# %%
# validFiles = validFiles.apply(lambda x: storeBase64(x), axis=1)
# %% [markdown]
# ## prepare text for LDA

# %%
# validFiles['text'] = validFiles['raw'].apply(lambda x: getTextFromCells(x))
# validText = validFiles.dropna()
# validText = validText['text'].apply(lambda x: getPlainText(x))
# logger.info("files with parsable markdown text  ")
# logger.info(validText.count())
# validText = validText.dropna()
# %%

# text.translate(str.maketrans('', '', string.punctuation))
# text =  re.sub('[,\.!?%=+-/#$:;]', '', text)
# print(len(text))
# %% [markdown]
# ## get notebooks with the most number of images

# This is to test if pa11y can catch visualization inaccessibility errors
#%%
# get the file name of the notebook with the most numImages
# %%
# fileMaxImages = validFiles[validFiles['numImages'] == validFiles['numImages'].max()]['fileNames'].values[0]
# logger.info("file with the most images is " + fileMaxImages)
# # use pypandoc and convert this notebook into html
# with open("data-1k/"+fileMaxImages, "r") as f:
#     html = pypandoc.convert_file("data-1k/"+fileMaxImages, 'html', format='ipynb')
#     with open("data-1k/"+fileMaxImages+".html", "w") as fh:
#         fh.write(html)

# %% [markdown]
# # cleanup and save.
# %%
validFiles = validFiles.drop(['raw', 'source', 'output', 'images'], axis=1)
print(validFiles)

validFiles.to_csv('nb_subplots.csv', header=True, index=False)

# write text into a text file
# with open('nbText.txt', 'w') as f:
#     f.write(text)

# validFilesRdd = spark.createDataFrame(validFiles).rdd
# logger.info(validFilesRdd.show())