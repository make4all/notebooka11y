# Data Processing Pipeline

The various scripts listed here perform the data processing:

1. `fetch_a11y_responses.py`
   - This script expects `pa11y` to be executed and the results stored in a separate directory.
   - For the pipeline we store the results from the executions of `pa11y` in the `pa11y-results/` directory.
   - Input Requirements:
     - `BASE_PA11Y_RESULT_DIR`: The base directory where the results from the `pa11y` scans are stored. (eg. `pa11y-results/`)
     - `THEMES`: The set of themes being used to analyze. It is set to `['darcula', 'dark', 'horizon', 'light', 'material-darker', 'solarized']`
   - The result of this script is the following intermediate datasets over which additional analysis is run.
     - `data_out/a11y-aggregate-scan.csv` with the structure containing the following columns:
       - ID
       - Notebook
       - Theme
       - Standard
       - Date
       - Total
       - Errors
       - Warnings
       - Notices
     - `data_out/a11y-detailed-result.csv` with the structure containing the individual details of each error in the notebook and stored in a long table format with the following columns:
       - ID
       - Notebook
       - Theme
       - Runner
       - Type
       - TypeCode
       - DetailCode
       - Selector
       
     > :warning: The detailed result file can be really large (> 60 GB) and can be time-consuming to construct. We share this dataset from our scans for future research efforts.

   > :heavy_check_mark: For the paper, the execution of the pipeline processes 589746 `pa11y` scan results in 59 chunks and takes **2833.13** seconds (46 minutes) to generate the resulting datasets for further analysis on a 72 core vCPU AWS c5.18xlarge instance.

2. `generate_accessibility_error_count.py`
3. `classify_images.py`
   - This script uses the `FV-CNN+FC-CNN` based model (included at `model/epoch_9_loss_0.04706_testAcc_0.96867_X_resnext101_docSeg.pth`) and classifies the images in various notebooks into 28 different categories.
   - The execution of this script requires all the images/plots in the notebooks to be stored in their `base64` file formats in a single directory. (eg. `data-100k/base64Images/`)
   - During its execution the script loads the model on the GPU/CPU devices as available and configured and classifies all images.
   - Input Requirements:
     - `MODEL_PATH`: The trained FV-CNN+FC-CNN model to use
     - `IMAGE_STORE`: The directory containing all the `base64` encoded images as files.
   - The result of this script is the following intermediate dataset:
     - `data_out/model-result.csv` which contains the following columns:
       - `Name`: Path to the image of the format `prefix/<notebook_name>.ipynb-<index>.<image_extension>`
       - `Notebook Name`
       - `Category`: A single category classification among the 28 available with the highest prediction accuracy.
   
   > :warning: To analyze `342722` images on multiple GPUs the model can take hours after the dataset is sharded appropriately. Non sharded inference can take over a day. Exercise caution while running this task.