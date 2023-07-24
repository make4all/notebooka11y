# Notebooks Considered in Study

The `100k-dataset.csv` file in this directory contains the names of the notebooks used in our analysis presented in the
paper. The dataset was randomly sampled and chosen from the larger 10M notebook dataset released and maintained by JetBrains.

10M Dataset: https://github-notebooks-samples.s3-eu-west-1.amazonaws.com/ntbs_list.json (511 MB)

> :warning: Please note the above dataset is a single large JSON file of 500 MB and could crash webpages or slow down the browser.

The 100k dataset was chosen randomly by selecting the list of filenames from the list provided, shuffling them and picking the required number.
This can be achieved by running the following bash command after installing the required tools `jq` and `shuf`.

```shell
$ curl -o ntbs_list.json https://github-notebooks-samples.s3-eu-west-1.amazonaws.com/ntbs_list.json # Download the available 10M filenames
$ cat ntbs_list.json | jq -r . | shuf | head -n 100000 > 100k-dataset.csv
```

The resulting dataset of 100K notebooks used in our study is 4.7 MB in size.
