import argparse
from concurrent.futures import ThreadPoolExecutor

from torchvision import models
from PIL import Image
import time
import torch.nn as nn
import torch

import torchvision.transforms as standard_transforms
import os
import base64
import io
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--chunk', dest='chunk', type=int, const=0, help='Device and Chunk ID')
args = parser.parse_args()

print('Attempting to use CUDA GPU ', args.chunk)
chunk = args.chunk

device = torch.device(f"cuda:{chunk}" if torch.cuda.is_available() else "cpu")

# Change paths as required to a directory/model where the input files are stored from previous pipeline executions
MODEL_PATH = '../model/epoch_9_loss_0.04706_testAcc_0.96867_X_resnext101_docSeg.pth'
IMAGE_STORE = 'data-100k/base64Images/'

labelNames = ['3D objects',
              'Algorithm',
              'Area chart',
              'Bar plots',
              'Block diagram',
              'Box plot',
              'Bubble Chart',
              'Confusion matrix',
              'Contour plot',
              'Flow chart',
              'Geographic map',
              'Line Chart',
              'Heat map',
              'Histogram',
              'Mask',
              'Medical images',
              'Natural images',
              'Pareto charts',
              'Pie chart',
              'Polar plot',
              'Radar chart',
              'Scatter plot',
              'Sketches',
              'Surface plot',
              'Tables',
              'Tree Diagram',
              'Vector plot',
              'Venn Diagram']


def fig_classification(fig_class_model_path):
    fig_model = models.resnext101_32x8d()
    num_features = fig_model.fc.in_features
    fc = list(fig_model.fc.children())  # Remove last layer
    fc.extend([nn.Linear(num_features, 28)])  # Add our layer with 4 outputs
    fig_model.fc = nn.Sequential(*fc)
    fig_model = fig_model.to(device)
    fig_model.load_state_dict(torch.load(fig_class_model_path, map_location=device))
    fig_model.eval()
    mean_std = ([.485, .456, .406], [.229, .224, .225])
    fig_class_transform = standard_transforms.Compose([
        standard_transforms.Resize((384, 384), interpolation=Image.ANTIALIAS),
        standard_transforms.ToTensor(),
        standard_transforms.Normalize(*mean_std)])
    return fig_model, fig_class_transform


fig_model, fig_class_transform = fig_classification(MODEL_PATH)

image_dir = IMAGE_STORE
image_paths = os.listdir(image_dir)
image_paths = [os.path.join(image_dir, p) for p in image_paths]

image_paths.sort()

print(f'Classifying information of {len(image_paths)} figures')

classifications = []
failed = []


def classify(img_path):
    try:
        with open(img_path, 'r') as f:
            base64image = f.read()
        base64decoded = base64.b64decode(base64image)
        image = Image.open(io.BytesIO(base64decoded)).convert('RGB')
        img_tensor = fig_class_transform(image)
        if torch.cuda.is_available():
            fig_label = fig_model(img_tensor.cuda().unsqueeze(0))
        else:
            fig_label = fig_model(img_tensor.unsqueeze(0))
        fig_prediction = fig_label.max(1)[1]
        classification = (img_path, labelNames[fig_prediction])
        return classification, None
    except Exception as e:
        print('Failed with exception: ', e)
        return None, img_path


start_time = time.time()
with ThreadPoolExecutor(max_workers=2) as executor:
    for classification, fail in executor.map(classify, image_paths):
        classifications.append(classification)
        failed.append(fail)
end_time = time.time()

print(f'Total time taken to classify: {end_time - start_time} seconds')

df = pd.DataFrame([[n[0], n[0].split('.ipynb')[0], n[1]] for n in classifications if n is not None],
                  columns=['Name', 'NotebookName', 'Category'])

df.to_csv(f'data_out/model-results.csv', header=True, index=False)
