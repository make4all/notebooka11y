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