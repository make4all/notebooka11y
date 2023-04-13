from concurrent.futures import ThreadPoolExecutor

import pandas

import requests

"""
Items to want:

1. How many errors across themes are overlapping and what are they?
    a. Where are they occurring?
2. What are the different types of errors? Distributions?
3. What is the distribution of errors per template?
"""

BASE_URL = 'http://localhost:3000/'


def obtain_tasks():
    path = 'tasks'
    query_url = BASE_URL + path
    data = requests.get(query_url)
    return data.json()


def get_task_information(task_item):
    SERVICE_URL = f"https://localhost:3000/tasks/{task_item['id']}/results?full=True"
    response = requests.get(SERVICE_URL)
    return convert_result(task_item, response.json())


def convert_result(task_item, result):
    if len(result) <= 0:
        print(f'No response for {task_item["name"]} in scan. Skipping ...')
        return [], []
    result_dict = result[0]
    taskname = task_item['name']
    theme, fname = taskname.split('--')
    standard = task_item['standard']
    id = result_dict['id']
    date = result_dict['date']
    total_count = result_dict['count']['total']
    error_count = result_dict['count']['error']
    warning_count = result_dict['count']['warning']
    notice_count = result_dict['count']['notice']

    scan_results = result_dict['results']

    result_joiner = []
    for scan_result in scan_results:
        runner = scan_result['runner']
        result_type = scan_result['type']
        result_type_code = scan_result['typeCode']
        scan_result_code = scan_result['code']
        scan_selector_affected = scan_result['selector']

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


if __name__ == '__main__':
    task_list = obtain_tasks()
    aggregate_data = []
    detailed_dfs = []

    aggregate_row_schema = ['ID', 'Notebook', 'Theme', 'Standard', 'Date', 'Total', 'Errors', 'Warnings', 'Notices']
    detailed_result_schema = ['ID', 'Notebook', 'Theme', 'Runner', 'Type', 'TypeCode', 'DetailCode', 'Selector']

    with ThreadPoolExecutor(max_workers=32) as executor:
        for response in list(executor.map(get_task_information, task_list)):
            aggregate_info, detailed_result = response
            if len(aggregate_info) > 0:
                ddf = pandas.DataFrame(data=detailed_result, columns=detailed_result_schema)
                aggregate_data.append(aggregate_info)
                detailed_dfs.append(ddf)

    agg_df = pandas.DataFrame(data=aggregate_data, columns=aggregate_row_schema)
    agg_df.to_csv('a11y-aggregate-scan.csv', header=True, index=False)

    detailed_df = pandas.concat(detailed_dfs)
    detailed_df.to_csv('a11y-detailed-result.csv', header=True, index=False)
