from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import os
import glob
import pandas
import json
import csv

import requests
from hashlib import sha256

"""
Items to want:

1. How many errors across themes are overlapping and what are they?
    a. Where are they occurring?
2. What are the different types of errors? Distributions?
3. What is the distribution of errors per template?
"""

BASE_URL = 'http://localhost:3000/'
BASE_PA11Y_RESULT_DIR = 'pa11y-results/'
THEMES = ['darcula', 'dark', 'horizon', 'light', 'material-darker', 'solarized']

def obtain_tasks():
    # path = 'tasks'
    # query_url = BASE_URL + path
    files_to_parse = glob.glob(f'{BASE_PA11Y_RESULT_DIR}**/*.json')
    # data = requests.get(query_url)
    return files_to_parse


def get_task_information(task_item):
    with open(task_item, 'r') as f:
        try:
            data = json.load(f)
            return convert_result(task_item, data)
        except Exception as e:
            print(f'failed to parse {task_item}. Continuing...')
            return [], []
    # SERVICE_URL = f"https://localhost:3000/tasks/{task_item['id']}/results?full=True"
    # response = requests.get(SERVICE_URL)
    # return convert_result(task_item, response.json())


def extract_information(filepath):
    id_string = sha256(filepath.encode('utf-8')).hexdigest()
    items = filepath.split('/')
    filename_with_extension = items[-1]
    theme = items[-2]
    filename, extension = filename_with_extension.split('.')
    return {'name': f'{filename}.ipynb', 'theme': theme, 'standard': 'WCAG2AA', 'id': id_string}


def convert_result(task_item, result):
    if len(result) <= 0:
        print(f'No response for {task_item["name"]} in scan. Skipping ...')
        return [], []
    info = extract_information(task_item)
    theme = info['theme']
    fname = info['name']
    standard = info['standard']
    id = info['id']
    date = None
    total_count = len(result)
    error_count = 0
    warning_count = 0
    notice_count = 0

    scan_results = result

    result_joiner = []
    for scan_result in scan_results:
        runner = scan_result['runner']
        result_type = scan_result['type']
        result_type_code = scan_result['typeCode']
        scan_result_code = scan_result['code']
        scan_selector_affected = scan_result['selector']

        if result_type == "error":
            error_count += 1
        if result_type == "warning":
            warning_count += 1
        if result_type == "notice":
            notice_count += 1

        result_joiner.append([
            id,
            fname,
            theme,
            runner,
            result_type,
            result_type_code,
            scan_result_code,
            scan_selector_affected
        ])

    return [
        id,
        fname,
        theme,
        standard,
        date,
        total_count,
        error_count,
        warning_count,
        notice_count
    ], result_joiner



def listener(q):
    aggreate_row_schema = ['ID', 'Notebook', 'Theme', 'Standard', 'Date', 'Total', 'Errors', 'Warnings', 'Notices']
    detailed_result_schema = ['ID', 'Notebook', 'Theme', 'Runner', 'Type', 'TypeCode', 'DetailCode', 'Selector']
    with open('a11y-aggregate-scan.csv', 'w') as f_a, open('a11y-detailed-result.csv', 'w') as f_d:
        wr_fa = csv.writer(f_a)
        wr_fd = csv.writer(f_d)
        wr_fa.writerow(aggregate_row_schema)
        wr_fd.writerow(detailed_result_schema)
        while 1:
            m = q.get()
            if m == 'kill':
                break


if __name__ == '__main__':
    task_list = obtain_tasks()
    print(f'Processing a total of {len(task_list)} files')

    aggregate_data = []
    detailed_dfs = []

    num_cpu = mp.cpu_count()

    manager = mp.Manager()
    q = manager.Queue()

    # task_list = task_list[:1000]

    aggregate_row_schema = ['ID', 'Notebook', 'Theme', 'Standard', 'Date', 'Total', 'Errors', 'Warnings', 'Notices']
    detailed_result_schema = ['ID', 'Notebook', 'Theme', 'Runner', 'Type', 'TypeCode', 'DetailCode', 'Selector']
    with open('a11y-aggregate-scan.csv', 'w') as f_a, open('a11y-detailed-result.csv', 'w') as f_d:
        wr_fa = csv.writer(f_a)
        wr_fd = csv.writer(f_d)
        wr_fa.writerow(aggregate_row_schema)
        wr_fd.writerow(detailed_result_schema)

    n = 10000
    task_list_chunks = [task_list[i:i + n] for i in range(0, len(task_list), n)]

    for index, task_list in enumerate(task_list_chunks):
        print(f'Processed Batch {index}/{len(task_list_chunks)}')
        with open('a11y-aggregate-scan.csv', 'a') as f_a, open('a11y-detailed-result.csv', 'a') as f_d:
            wr_fa = csv.writer(f_a)
            wr_fd = csv.writer(f_d)
            # wr_fa.writerow(aggregate_row_schema)
            # wr_fd.writerow(detailed_result_schema)
            with ThreadPoolExecutor(max_workers=num_cpu) as executor:
                for response in list(executor.map(get_task_information, task_list)):
                    aggregate_info, detailed_result = response
                    if len(aggregate_info) > 0:
                        wr_fa.writerow(aggregate_info)
                        wr_fd.writerows(detailed_result)
                        # ddf = pandas.DataFrame(data=detailed_result, columns=detailed_result_schema)
                        # aggregate_data.append(aggregate_info)
    
    print('Processing complete')

    # agg_df = pandas.DataFrame(data=aggregate_data, columns=aggregate_row_schema)
    # agg_df.to_csv('a11y-aggregate-scan.csv', header=True, index=False)

    # detailed_df = pandas.concat(detailed_dfs)
    # detailed_df.to_csv('a11y-detailed-result.csv', header=True, index=False)

