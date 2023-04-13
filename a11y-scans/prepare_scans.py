from concurrent.futures import ThreadPoolExecutor
from io import StringIO

from urllib.parse import urlparse
import requests

from lxml import etree

BASE_URI = 'http://localhost:8080/'


def get_links_from_page(url):
    parser = etree.HTMLParser()
    data = requests.get(url)
    html_string = data.content.decode("utf-8")
    tree = etree.parse(StringIO(html_string), parser=parser)
    links = tree.xpath("//a/text()")
    links = [l.strip('/') for l in links]
    return links


def create_scanner_input_list():
    available_directories = get_links_from_page(BASE_URI)
    scanner_input = []
    for directory in available_directories:
        files_available_req = BASE_URI + directory + '/'
        file_names = get_links_from_page(files_available_req)
        for file_name_to_scan in file_names:
            available_paths = files_available_req + file_name_to_scan
            scanner_input.append(available_paths)

    with open('a11y-scans/scan-requests.csv', 'w') as f:
        for query in scanner_input:
            f.write(query + '\n')
    f.close()


def create_scan_task(url):
    SERVICE_URI = "http://localhost:3000/"
    endpoint = "tasks"
    uri = urlparse(url)
    path_elements = uri.path.split('/')
    scan_mode, filename = path_elements[1], path_elements[2]
    request_payload = {
        'name': scan_mode + '--' + filename.split('.html')[0],
        'url': url,
        'standard': 'WCAG2AA',
        'actions': [],
    }
    resp = requests.post(SERVICE_URI + endpoint, request_payload)
    return resp.json()


def run_task(taskid):
    SERVICE_URI = f"http://localhost:3000/tasks/{taskid}/run"
    resp = requests.post(SERVICE_URI, None)
    return resp.status_code


def run_tasks(task_list):
    with ThreadPoolExecutor(max_workers=32) as executor:
        for response in list(executor.map(run_task, task_list)):
            print(response)


if __name__ == '__main__':
    create_scanner_input_list()

    counter = 0
    with open('a11y-scans/scan-requests.csv', 'r') as f:
        data = f.readlines()

    task_ids = []
    for i, url in enumerate(data):
        if i % 100 == 0:
            print(f'Created scan tasks for {i+1} notebooks')
        task_response = create_scan_task(url)
        id = task_response['id']
        task_ids.append(id)

    run_tasks(task_list=task_ids)

