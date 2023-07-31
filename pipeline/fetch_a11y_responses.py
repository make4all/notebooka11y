from concurrent.futures import ThreadPoolExecutor
import csv
import glob
import json
import multiprocessing as mp
import time

from hashlib import sha256


BASE_PA11Y_RESULT_DIR = 'pa11y-results/'
THEMES = ['darcula', 'dark', 'horizon', 'light', 'material-darker', 'solarized']
aggregate_row_schema = ['ID', 'Notebook', 'Theme', 'Standard', 'Date', 'Total', 'Errors', 'Warnings', 'Notices']
detailed_result_schema = ['ID', 'Notebook', 'Theme', 'Runner', 'Type', 'TypeCode', 'DetailCode', 'Selector']


def obtain_tasks():
    '''
    Returns the list of files to be processed
    '''
    files_to_parse = glob.glob(f'{BASE_PA11Y_RESULT_DIR}**/*.json')
    return files_to_parse


def get_task_information(task_item):
    '''
    Loads the file and returns the converted results into the required format #TODO: is this correct?

    Parameters
    ----------
        task_item : str
            The path of the file to be processed
    '''
    with open(task_item, 'r') as f:
        try:
            data = json.load(f)
            return convert_result(task_item, data)
        except Exception as e:
            print(f'failed to parse {task_item}. Continuing...')
            return [], []


def extract_information(filepath):
    '''
    Extracts the information from the filepath and returns the information of
    the file, theme, A11Y standard in a python dictionary

    Parameters
    ----------
        filepath : str
            The path of the file to be processed
    '''
    id_string = sha256(filepath.encode('utf-8')).hexdigest()
    items = filepath.split('/')
    filename_with_extension = items[-1]
    theme = items[-2]
    filename, extension = filename_with_extension.split('.')
    return {'name': f'{filename}.ipynb', 'theme': theme, 'standard': 'WCAG2AA', 'id': id_string}


def convert_result(task_item, result):
    '''
    Converts and returns the result of the pa11y scan into the required format

    Parameters
    ----------
        task_item : str
            The path of the file to be processed
        result : dict
            The result of the pa11y scan
    '''
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


if __name__ == '__main__':
    # Obtain the list of output results files after the pa11y scans.
    task_list = obtain_tasks()
    print(f'Processing a total of {len(task_list)} files')

    aggregate_data = []
    detailed_dfs = []

    num_cpu = mp.cpu_count()

    manager = mp.Manager()

    AGG_RESULT_PATH = 'data_out/a11y-aggregate-scan.csv'
    DETAILED_RESULT_PATH = 'data_out/a11y-detailed-result.csv'

    # Create the necessary output files and add the CSV header structure into it.
    with open(AGG_RESULT_PATH, 'w') as f_a, open(DETAILED_RESULT_PATH, 'w') as f_d:
        wr_fa = csv.writer(f_a)
        wr_fd = csv.writer(f_d)
        wr_fa.writerow(aggregate_row_schema)
        wr_fd.writerow(detailed_result_schema)

    # Split the processing into chunks of 10000 elements each.
    n = 10000
    task_list_chunks = [task_list[i:i + n] for i in range(0, len(task_list), n)]

    start_time = time.time()
    # Batch-wise process the results from pa11y and write the responses from the parallel threads into the datasets.
    for index, task_list in enumerate(task_list_chunks):
        print(f'Processed Batch {index}/{len(task_list_chunks)}')
        with open(AGG_RESULT_PATH, 'a') as f_a, open(DETAILED_RESULT_PATH, 'a') as f_d:
            wr_fa = csv.writer(f_a)
            wr_fd = csv.writer(f_d)
            with ThreadPoolExecutor(max_workers=num_cpu) as executor:
                for response in list(executor.map(get_task_information, task_list)):
                    aggregate_info, detailed_result = response
                    if len(aggregate_info) > 0:
                        wr_fa.writerow(aggregate_info)
                        wr_fd.writerows(detailed_result)

    print('Processing complete')
    end_time = time.time()
    print(f'Time Taken: {end_time - start_time} seconds')
