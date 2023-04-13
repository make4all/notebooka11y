import os
from collections import defaultdict
import requests
from multiprocessing import Pool, cpu_count
from functools import partial
from io import BytesIO
import pandas


OUTPUT_DIR = 'data-10k/'

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
    df = pandas.read_csv('sample-10000.txt', names=['Filename'])

    urls = []
    for i, row in df.iterrows():
        urls.append(row['Filename'])

    pool = Pool(cpu_count())
    download_method = partial(download_notebook)
    results = pool.map(download_method, urls)
    pool.close()
    pool.join()


main()

