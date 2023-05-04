import base64
from io import BytesIO
from PIL import Image
from transformers import Pix2StructForConditionalGeneration, Pix2StructProcessor
from optimum.bettertransformer import BetterTransformer
import csv
import time 
# setup huggingface DePlot prediction run
def setupDePlot():
    model = Pix2StructForConditionalGeneration.from_pretrained('google/deplot').to("cuda:0")
    # better_model = BetterTransformer.transform(model)
    processor = Pix2StructProcessor.from_pretrained('google/deplot')#.to("cuda:0")
    print('model and processor loaded')
    # return model and processors
    return model, processor

# decode base64 string into image and open using pil

def imageToText(imageFileName,model, processor):
    with open(imageFileName, 'r') as f:
        print(f"imageFileName: {imageFileName}")
        base64String = f.read()
        img = Image.open(BytesIO(base64.b64decode(base64String)))
        tick = time.perf_counter()
        inputs = processor(images=img, text="Generate underlying data table of the figure below:", return_tensors="pt")
        inputs.to("cuda:0")
        predictions = model.generate(**inputs, max_new_tokens=512)
        print(processor.decode(predictions[0], skip_special_tokens=True))
        tock = time.perf_counter()
        t = tock-tick
        print(f"time taken for inference is {t}")
    
        return processor.decode(predictions[0], skip_special_tokens=True)

if __name__ == '__main__':
    predictions = []
    imageList = ['00014130779110127e4663c5bea956ca980c3294.ipynb-5.png', '00082fcf492642b59673fd1ff66541e1ae122ca5.ipynb-2.png','003e20d8f7c57bf64c4ed44576bf206b4a101bd0.ipynb-3.png','00678dbd68eb28db8017713742d0a9dd3931fbec.ipynb-5.png','00adf67eebbead5e371a004e6968660ecd7612a8.ipynb-10.png','00c0becc7875f0697a043924d3c615ae6e354136.ipynb-20.png']
    model, processor = setupDePlot()
    for image in imageList:
        prediction = {}
        prediction['image'] = image
        prediction['table'] = imageToText('data-100k/base64Images/'+image,model,processor)
        predictions.append(prediction)
    print("predictions complete")
    # write predictions to csv
    # with open('DePlotPredictions.csv', 'w') as f:
    #     headers = ['image','prediction']
        # # write predictions and headers to csv
        # writer = csv.DictWriter(f, fieldnames=headers)
        # writer.writeheader()
        # for prediction in predictions:
        #     writer.writerow(prediction.values())

        # print("csv file entry complete")

