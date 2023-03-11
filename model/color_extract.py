import json

import pandas
import pandas as pd
import base64
import os
import io
import numpy
import scipy
from PIL import Image
import matplotlib

image_dir = 'data-1k/base64Images/'
image_paths = os.listdir(image_dir)
image_paths = [os.path.join(image_dir, p) for p in image_paths]


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def color_2_hex(color_list):
    res = []
    for color_item in color_list:
        count, color = color_item
        c = rgb_to_hex(color)
        res.append((count, c))
    return res


classifications = []

for count, img_path in enumerate(image_paths):
    if count % 1000 == 0:
        print(f'Processed {count}/{len(image_paths)}')
    try:
        with open(img_path, 'r') as f:
            base64image = f.read()
        base64decoded = base64.b64decode(base64image)
        image = Image.open(io.BytesIO(base64decoded)).convert('RGB')
        colors_used = image.getcolors(maxcolors=1_000_000)
        classifications.append((img_path, len(colors_used), json.dumps(color_2_hex(colors_used))))
    except Exception as e:
        print(e)


df = pandas.DataFrame(data=classifications, columns=['ImageID', 'NumColors', 'Colors'])
df.to_csv('colors_in_figures.csv', header=True, index=False)
