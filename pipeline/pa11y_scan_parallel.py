from collections import defaultdict
import glob
import multiprocessing
from multiprocessing.pool import ThreadPool
import os
import subprocess

THEMES = ['darcula', 'dark', 'horizon', 'light', 'material-darker', 'solarized']

BASE_OUT_DIR_PA11Y = 'pa11y-results/'

SERVING_DIRECTORY = 'serve/'


def filename_extractor(filepath):
    '''
    Extracts the filename and theme from the filepath
    and returns the filename in the format of {filename}.json and the theme

    Parameters
    ----------
        filepath : str
            The path of the file to be processed
    '''
    items = filepath.split('/')
    filename_with_extension = items[-1]
    theme = items[-2]
    filename, extension = filename_with_extension.split('.')
    return f'{filename}.json', theme


def prepare_output_directories():
    '''
    Returns the commands to create the output directories for the pa11y results 
    of each theme
    '''
    command = [['mkdir', '-p', f'{BASE_OUT_DIR_PA11Y}{theme}'] for theme in THEMES]
    return command


def prepare_subcommand(in_filepath, out_filepath):
    '''
    Returns the command to execute pa11y in the given format on the given file

    Parameters
    ----------
        in_filepath : str
            The path of the file to be processed
        out_filepath : str
            The path of the file to be written to
    '''
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
    '''
    Executes the given command

    Parameters
    ----------
        command : list
            The command to be executed
    '''
    out_file_path = command[-1]
    command = command[:-2]  # Trim the last two arguments of the command line query
    with open(out_file_path, 'w') as out_file_on_disk:
        subprocess.run(command, stdout=out_file_on_disk)


def run_in_batches(batch_size, executable_commands):
    '''
    Executes the given commands in batches of the given size

    Parameters
    ----------
        batch_size : int
            The size of the batch to be executed
        executable_commands : list
            The commands to be executed
    '''
    with ThreadPool(batch_size) as pool:
        pool.map(scan, executable_commands)


def find_actual_paths(json_response_path):
    '''
    Returns the path of the html file that corresponds to the given JSON result file

    Parameters
    ----------
        json_response_path : str
            The path of the json file to be processed
    '''
    segments = json_response_path.split('/')
    html_file_path = f'{SERVING_DIRECTORY}{segments[1]}/{segments[2]}'
    html_file_path = html_file_path.replace('.json', '.html')
    return html_file_path


def find_empty_file_results():
    '''
    Returns a dictionary of the empty files and their corresponding html path of each theme
    '''
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
    creation_commands = prepare_output_directories()
    run_in_batches(len(creation_commands), creation_commands)

    file_paths = []
    empty_files = find_empty_file_results()
    for k, v in empty_files.items():
        for filepath in v:
            file_paths.append(filepath)

    num_cpu = multiprocessing.cpu_count()
    print(f'Using {num_cpu} CPU cores')
    print(f'Number of files: {len(file_paths)}')
    commands = []
    for f in file_paths:
        output_filename, theme = filename_extractor(f)
        out_file_path = f'{BASE_OUT_DIR_PA11Y}{theme}/{output_filename}'
        command = prepare_subcommand(f, out_file_path)
        commands.append(command)

    print(f'Number of commands to execute: {len(commands)}')
    run_in_batches(num_cpu, commands)


main()
