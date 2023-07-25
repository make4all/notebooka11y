# NotablyInaccessible–Data Driven Understanding of Data Science Notebook (In)Accessibility
[Venkatesh Potluri\*](https://venkateshpotluri.me/), [Sudheesh Singanamalla\*](https://sudheesh.info/), [Nussara Tieanklin](https://nussarafirn.github.io/), [Jennifer Mankoff](https://www.cs.washington.edu/people/faculty/jmankoff)

\* Both authors contributed equally to this effort.

## Overview
Computational notebooks, tools that facilitate storytelling through exploration, data analysis, and information visualization, have become the widely accepted standard in the data science community. These notebooks have been widely adopted through 
notebook software such as [Jupyter](https://jupyter.org/), [Datalore](https://www.jetbrains.com/datalore/) and [Google Colab](https://colab.research.google.com/), both in academia and industry.  While there is extensive research to learn  how data scientists use computational notebooks, identify their pain points, and enable collaborative data science practices, very little is known about the various accessibility barriers experienced by blind and visually impaired (BVI) users using these notebooks. BVI users are unable to use computational notebook interfaces due to inaccessibility of the interface, common ways in which data is represented in these interfaces, and inability for popular libraries to provide accessible outputs.

We perform a large scale systematic analysis of a randomly chosen set of 100000 Jupyter notebooks, a subset of a large [dataset of ten million notebooks](https://blog.jetbrains.com/datalore/2020/12/17/we-downloaded-10-000-000-jupyter-notebooks-from-github-this-is-what-we-learned/) provided by JetBrains, to identify various accessibility challenges in published notebooks affecting the creation and consumption of these notebooks. Through our findings, we make recommendations to improve accessibility of the artifacts of a notebook, suggest authoring practices, and propose changes to infrastructure to make notebooks accesible. Please read our paper to gain an in-depth understanding of our findings.

This repository contains the processing and reproducibility scripts for the results of the paper.

## Repository Contents

This repository contains two artifacts and depends on a third, externally hosted dataset:
1. A [set of notebooks](https://make4all.github.io/notebooka11y) to reproduce the data-driven results that we present in the paper.
2. The [pipeline](pipeline/readme.md) that we built to process and analyse the 100K notebooks.
3. [Datasets](input_data/readme.md) that are necessary to run the pipeline. These are hosted on Zenodo.

## Attribution
If this work inspires yours, consider citing us as follows:
### ACM Reference Format (End Note)

Venkatesh Potluri, Sudheesh Singanamalla, Nussara Tieanklin, Jennifer Mankoff. 2023. Notably Inaccessible -- Data Driven Understanding of Data Science Notebook (In)Accessibility. In the 25th International ACM SIGACCESS Conference on Computers and Accessibility (ASSETS '23). October 22-25, 2023, New York, NY, USA. ACM, New York, NY, USA, 18 pages. https://doi.org/10.1145/3597638.3608417

### LaTeX

<pre>
@inproceedings{10.1145/3597638.3608417,
    author = {Potluri, Venkatesh and Singanamalla, Sudheesh and Tieanklin, Firn and Mankoff, Jennifer},
    title = {Notably Inaccessible – Data Driven Understanding of Data Science Notebook (In)Accessibility},
    year = {2023},
    isbn = {979-8-4007-0220-4/23/10},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3597638.3608417},
    booktitle = {Proceedings of the 25th International ACM SIGACCESS Conference on Computers and Accessibility},
    location = {New York, NY, USA},
    series = {ASSETS '23}
}
</pre>

## Accessibility Notes

As our findings show, a majority of the necessary tools to perform a large scale analysis of this nature are inaccessible. We however exercised care to the best extent possible to share screen-reader accessible artifacts. Please reach out to us if you run into accessibility issues or have suggestions to improve the accessibility of this artifact and we will do our best to make things accessible. We are including a few screen reader accessibility tips that we feel may be useful when working with this dataset using a screen reader.
1. working with notebooks. As we find out from this research, you may run into a variety of accessibility issues with them. We recommend using VS Code to read through the cell content of the notebooks we share. We recommend exporting the notebooks to HTML if you wish to  access the outputs as well. VS Code comes with the ability to provide audio notifications to indicate the completion of a cell's execution, and if the completion is successful. We recommend running the notebooks one cell at a time.
2. Exporting notebooks. An alternate accessible workflow to work with notebooks would be to export them to python scripts. Informed by the experience of our team member who uses a screen reader, this especially may be helpful to edit code. We recommend using the [percent format](https://jupytext.readthedocs.io/en/latest/formats-scripts.html) as it may be easy to read, and is well supported by a variety of IDEs including VS Code.
3. working with Python scripts. Most of our pipeline contains standard python scripts. Some of these scripts however may take time to run so please refer to the provided [documentation](pipeline/readme.md) carefully before running the scripts. We provided time estimates for each script in our pipeline.
4. Working with our data. All of our data is formatted as comma separated values. Some files however may be large and can cause screen readers and IDEs to crash. While there is no threshold to identify crashes, we recommend running `wc -l 'file.csv'` to get an estimate of the number of rows in the file. An easy way to access the data columns of the file would be to run `head -n 'file.csv'`. This prints the first line of the csv file that contains the column headers.