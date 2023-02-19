# %% [markdown]
# # code to perform LDA.
# ## imports and setup

# %%
from tokenize import PlainToken
import string
import numpy as np
import logging
import nbformat
import json
import pandas as pd
import pandas as pd
import pypandoc

logging.basicConfig(filename="log/processNotebooks.log", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
text = ''
# %% [markdown]
# # lambdas.
# Please include lambdas in the cell below. You should run this cell if you add a new lambda.
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

# remove the punctuations from text and lower them to prepare for LDAModel
def processTextForLDA(txt):
    # re.sub('[,\.!?%=+-/]', '', x)
    txt.translate(str.maketrans('', '', string.punctuation))
# get all the plain text into one string
def getPlainText(textColumn):
    global text
    text = text+textColumn

# %% [markdown]
# Here, we will be using code from the processNotebooks to get markdown strings. replace these cells with updated code once I have access.
# # process notebooks
# %%
# load the text file into a pandas dataframe
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
logger.info("number of valid files")
logger.info(validFiles.count())
# validFiles.set_option('display.width', 999)
pd.options.display.max_colwidth = 999
# print(validFiles.count())

# now get the kernel type and language for each file and store it in the "language" column of this dataframe.
validFiles['language'] = validFiles['raw'].apply(lambda x: getLanguage(x) )
print(f'Shape of validfiles with lambda: {validFiles.shape}')
# logger.info(validFiles[['fileNames','language']].head(20))
validFiles= validFiles.dropna()
print(f'Validfiles with drop na : {validFiles.shape}')
# # gropup by language and store the count for each language in the df in a new column "count"
validFiles = validFiles[validFiles['language'].str.contains('py')]
print(f'Validfiles with language filter: {validFiles.shape}')
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

# %% [markdown]
# ## extracting text for LDA.
# Here, we use pandoc through pipandoc to extract text from the markdown cells of jupytor notebooks. We drop text from invalid markdown cells that pandoc is unable to process.
# %%
validFiles['text'] = validFiles['raw'].apply(lambda x: getTextFromCells(x))
validText = validFiles.dropna()
logger.info("files with parsable markdown text  ")
logger.info(validText.count())
validText = validText.dropna()

validText['preparedText'] = validText['text'].apply(lambda x: processTextForLDA(x))
validText = validText.dropna()
logger.info("valid files with text after removing punctuation")
logger.info(validText.count())

validText = validText['preparedText'].apply(lambda x: getPlainText(x))
logger.info("plain text from all files is ")
print(len(text))
logger.info(validText[['fileNames','language','numImages','preparedText']].head(5))