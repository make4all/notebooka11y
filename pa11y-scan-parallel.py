import multiprocessing
from multiprocessing.pool import ThreadPool
import os
import subprocess
import glob

from collections import defaultdict


THEMES = ['darcula', 'dark', 'horizon', 'light', 'material-darker', 'solarized']

BASE_OUT_DIR_PA11Y='pa11y-results/'

SERVING_DIRECTORY = 'serve/'


def filename_extractor(filepath):
    items = filepath.split('/')
    filename_with_extension = items[-1]
    theme = items[-2]
    filename, extension = filename_with_extension.split('.')
    return f'{filename}.json', theme


def prepare_output_directories():
    command = [['mkdir', '-p', f'{BASE_OUT_DIR_PA11Y}{theme}'] for theme in THEMES]
    return command


def prepare_subcommand(in_filepath, out_filepath):
    command = ['pa11y',
            '--standard',
            'WCAG2AA',
            '--reporter',
            'json',
            '--runner',
            'axe',
            '--runner',
            'htmlcs',
            '--include-notices',
            '--include-warnings',
            f'{in_filepath}',
            '>>',
            f'{out_filepath}'
            ]
    return command


def scan(command):
    out_file_path = command[-1]
    command = command[:-2]  # Trim the last two arguments of the command line query
    print(f'Processing {command[-1]} into {out_file_path}')
    with open(out_file_path, 'w') as out_file_on_disk:
        subprocess.run(command, stdout=out_file_on_disk)


def run_in_batches(batch_size, executable_commands):
    with ThreadPool(batch_size) as pool:
        pool.map(scan, executable_commands)


def find_actual_paths(json_response_path):
    segments = json_response_path.split('/')
    html_file_path = f'{SERVING_DIRECTORY}{segments[1]}/{segments[2]}'
    html_file_path = html_file_path.replace('.json', '.html')
    return html_file_path


def find_empty_file_results():
    empty_files = defaultdict(list)
    for theme in THEMES:
        files = glob.glob(f'{BASE_OUT_DIR_PA11Y}{theme}/*.json')
        for f in files:
            fsize = os.path.getsize(f)
            if fsize == 0:
                html_f = find_actual_paths(f)
                empty_files[theme].append(html_f)
    return empty_files


def main():
    # Output directory creation
    # creation_commands = prepare_output_directories()
    # run_in_batches(len(creation_commands), creation_commands)
    file_paths = []
    empty_files = find_empty_file_results()
    for k, v in empty_files.items():
        print(k, len(v), v[:5])
        for filepath in v:
            file_paths.append(filepath)

    num_cpu = multiprocessing.cpu_count()
    print(f'Using {num_cpu} CPU cores')
    # file_paths = glob.glob(f'{SERVING_DIRECTORY}**/*.html')
    print(f'Number of files: {len(file_paths)}')
    commands = []
    for f in file_paths:
        output_filename, theme = filename_extractor(f)
        out_file_path = f'{BASE_OUT_DIR_PA11Y}{theme}/{output_filename}'
        command = prepare_subcommand(f, out_file_path)
        commands.append(command)

    print(f'Number of commands to execute: {len(commands)}')
    # print(commands[:4])
    run_in_batches(num_cpu, commands)


main()

