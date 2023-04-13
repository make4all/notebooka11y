import os
import glob
from collections import defaultdict
import requests
from multiprocessing import Pool, cpu_count
from functools import partial
from io import BytesIO
import pandas
import json
from random import sample

OUTPUT_DIR = 'data-100k/'


def read_filenames():
    filepaths = glob.glob(f'{OUTPUT_DIR}*.ipynb')
    files = [f.split('/')[1] for f in filepaths]
    return set(files)


def download_notebook(notebook_name):
    notebook_url = f'https://github-notebooks-update1.s3-eu-west-1.amazonaws.com/{notebook_name}'
    try:
        print(f'Downloading {notebook_url}')
        data = requests.get(notebook_url)
        with open(f'{OUTPUT_DIR}{notebook_name}', 'w') as f:
            f.write(data.text)
        return True
    except:
        return False


def main():
    #with open('ntbs_list.json', 'r') as f:
    #    data = json.load(f)

    #NUM_RANDOM = 100000
    #items = sample(data, NUM_RANDOM)
    #print(len(items))

    #df = pandas.DataFrame(data=items, columns=['Filename'])
    #df.to_csv('sample-100000.csv', header=False, index=False)

    downloaded_files = read_filenames()

    df = pandas.read_csv('sample-100000.csv', names=['Filename'])
    files_to_download = set(df['Filename'].tolist())
    files_to_download = files_to_download.difference(downloaded_files)

    print(len(files_to_download))

    urls = []
    for i, filename in enumerate(list(files_to_download)):
        urls.append(filename)

    pool = Pool(cpu_count())
    download_method = partial(download_notebook)
    results = pool.map(download_method, urls)
    pool.close()
    pool.join()


main()


