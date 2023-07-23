from functools import partial
import glob
from multiprocessing import Pool, cpu_count
import os
import pandas
import requests


INPUT_DATASET = 'input_data/100k-dataset.csv'
OUTPUT_DIR = 'data-100k/'

os.makedirs(OUTPUT_DIR, exist_ok=True)


JETBRAINS_DATASTORE_ENDPOINT = 'https://github-notebooks-update1.s3-eu-west-1.amazonaws.com'


def read_filenames():
    filepaths = glob.glob(f'{OUTPUT_DIR}*.ipynb')
    files = [f.split('/')[1] for f in filepaths]
    return set(files)


def download_notebook(notebook_name):
    notebook_url = f'{JETBRAINS_DATASTORE_ENDPOINT}/{notebook_name}'
    try:
        data = requests.get(notebook_url)
        with open(f'{OUTPUT_DIR}{notebook_name}', 'w') as f:
            f.write(data.text)
        return True
    except:
        return False


def main():
    downloaded_files = read_filenames()

    df = pandas.read_csv(INPUT_DATASET, names=['Filename'])
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

