import json
from collections import defaultdict
from urllib.request import urlretrieve
from tqdm import tqdm
import pandas as pd
files = ['ntb_2020_consistency.csv', 'ntb_2020_from_mooc.csv', 'ntb_2020_imports.csv', 'ntb_2020_md_stats.csv',
         'ntb_2020_text_counts.csv', 'ntb_2020_versions.csv', '2019_imports_4128764_nbs.json']
with tqdm(total=len(files), desc='Downloading files') as pbar:
    for f in files:
        urlretrieve(f'https://github-notebooks-samples.s3-eu-west-1.amazonaws.com/{f}', f)
        pbar.update()