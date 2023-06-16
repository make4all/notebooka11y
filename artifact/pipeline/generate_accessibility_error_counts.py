from collections import defaultdict
import csv
import pandas as pd
import time

COLUMN_HEADERS = ['Type', 'Theme', 'Runner', 'DetailCode', 'count']
DETAILED_ERROR_REPORT_FILE = 'data_out/a11y-detailed-result.csv'

def analyseErrors(input_dataframe_filepath):
    notebook_theme_counter = defaultdict(set)

    print('Pass 1 - Identifying the correct notebooks to use')
    with open(input_dataframe_filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for i, line in enumerate(reader):
            if i % 10000:
                print(f'\tPass 1 - Processed {i} records')
            elements = dict(zip(header, line))
            notebook_name = elements['Notebook']
            theme = elements['Theme']

            notebook_theme_counter[notebook_name].add(theme)
    print('Completed first pass')

    print('Pass 2 - Performing the correct aggregations')
    theme_error_counter = {}
    with open(input_dataframe_filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for i, line in enumerate(reader):
            if i % 10000:
                print(f'Processed {i} records')
            
            elements = dict(zip(header, line))
            id = elements['ID']
            notebook_name = elements['Notebook']
            theme = elements['Theme']
            runner = elements['Runner']
            record_type = elements['Type']
            detail_code = elements['DetailCode']

            num_themes_for_notebook = len(notebook_theme_counter[notebook_name])
            if num_themes_for_notebook < 6:
                continue

            if record_type not in theme_error_counter:
                theme_error_counter[record_type] = {}
            if theme not in theme_error_counter[record_type]:
                theme_error_counter[record_type][theme] = {}
            if runner not in theme_error_counter[record_type][theme]:
                theme_error_counter[record_type][theme][runner] = {}
            if detail_code not in theme_error_counter[record_type][theme][runner]:
                theme_error_counter[record_type][theme][runner][detail_code] = 0
                
            # Increment the error count for the specific error
            theme_error_counter[record_type][theme][runner][detail_code] = theme_error_counter[record_type][theme][runner][detail_code] + 1

    
    row_result = []
    for record_type, record_indexed_data in theme_error_counter.items():
            for theme, theme_indexed_data in record_indexed_data.items():
                for runner, runner_indexed_data in theme_indexed_data.items():
                    for detail_code, count in runner_indexed_data.items():
                        row = [record_type, theme, runner, detail_code, count]
                        row_result.append(row)

    return pd.DataFrame(row_result, columns=COLUMN_HEADERS)

def analyzeSummary(df):
    # same as df but sorted
    df.groupby('DetailCode')\
        .filter(lambda x: x['count'].nunique() > 1)\
        .sort_values(by=['Type','Runner','count'], ascending=[True,True, False])\
        .to_csv('data_out/errors-different-counts-a11y-analyze-errors-summary.csv', index=False)
    print("file write of df with a filter to store errors that have different counts across themes to errors-different-counts-a11y-analyze-errors-summary.csv")


if __name__ == "__main__":
    start_time = time.time()
    
    df = analyseErrors(input_dataframe_filepath = DETAILED_ERROR_REPORT_FILE)
    analyzeSummary(df)

    print('Processing complete')
    end_time = time.time()
    print(f'Time Taken: {end_time - start_time} seconds')
