# Datasets & A Note on Reproducibility

[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8185050.svg)](https://doi.org/10.5281/zenodo.8185050)

> The authors have taken significant care to present this artifact and believe that this artifact is fully reproducible. Please reach out to the authors or open a github issue in case of challenges reproducing the results in the paper with the provided data or errors while executing the various stages in the pipeline as described [here](https://github.com/make4all/notebooka11y/tree/main/pipeline#pipeline-execution-plan).

The `data_out/` directory houses the resulting datasets from the pipeline executions.
For easy reproducibility, we share the intermediate datasets from our pipeline executions with the community.

This data can be found at the following [Zenodo](https://zenodo.org/record/8185050) link.

To reproduce the results and execute all the notebooks in this repository, please download the dataset presented as a 1.8 GB compressed file.
Extract the directory until you obtain the following files and place them in this `data_out/` directory.

```txt
a11y-aggregate-scan.csv
a11y-scan-dataset.zip
errors-different-counts-a11y-analyze-errors-summary.csv
model/
model-results.csv
nb_first_interactive_cell.csv
nb_processed_cell_html.csv
nb_processed.csv
processed_function_calls.csv
README.md
```

> :warning: While extracting the nested `a11y-scan-dataset.zip` directory is not required to reproduce the results in the notebooks. If required, please exercise caution while extracting, this results in a 60 GB file and could take a long time to extract.

Once the `csv` files are in the `data_out/` directory, The Jupyter notebooks can be re-executed to reproduce all the results and will update the existing results in `plot_out/` which are shared with the research community from our executions before being included in the research paper.
