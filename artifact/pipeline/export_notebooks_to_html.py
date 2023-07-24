import glob
import multiprocessing
from multiprocessing.pool import ThreadPool
import os
import subprocess


DATA_DIR='data-100k/'
OUTPUT_DIR = 'serve/'
THEMES = ['darcula', 'horizon', 'material-darker', 'solarized', 'light', 'dark']

THEME_CONVERSION_REPLACER = {
        'darcula': 'theme-darcula',
        'light': 'light',
        'horizon': 'jupyterlab-horizon-theme',
        'material-darker': 'jupyterlab_materialdarker',
        'solarized': 'jupyterlab-theme-solarized-dark',
        'dark': 'dark'
        }

def read_file_paths():
    files = glob.glob(f'{DATA_DIR}*.ipynb')
    files = [f.split('/')[1] for f in files]
    files.sort()
    return files


def setup_serving_themes():
    command = [['mkdir', '-p', f'{OUTPUT_DIR}{theme_name}'] for theme_name in THEMES]
    return command


def run_in_batches(batch_size, executable_commands):
    with ThreadPool(batch_size) as pool:
        pool.map(subprocess.run, executable_commands)

def create_nbconvert_commands(files, theme_list):
    executable_commands = []
    for file in files:
        for theme in theme_list:
            command = [
                    'jupyter',
                    'nbconvert',
                    f'{DATA_DIR}{file}',
                    '--to',
                    'html',
                    '--theme',
                    f'{THEME_CONVERSION_REPLACER[theme]}',
                    f'--output-dir={OUTPUT_DIR}{theme}'
                    ]
            executable_commands.append(command)
    return executable_commands


def find_failed_conversion_files(all_files_set):
    result = {}
    for theme in THEMES:
        files = set([f.replace('.html', '.ipynb') for f in os.listdir(f'{OUTPUT_DIR}/{theme}/') if '.html' in f])
        missing_files = all_files_set.difference(files)
        print(f'{theme} has {len(missing_files)} to convert')
        result[theme] = missing_files
    return result


def main():
    # Setup phase, create the necessary directories
    commands = setup_serving_themes()
    run_in_batches(len(commands), commands)

    # Prepare the commands to be executed
    files = read_file_paths()
    print(f'{len(files)} need to be converted into theme HTML')
    failed_files = find_failed_conversion_files(set(files))
    for theme, files in failed_files.items():
        commands = create_nbconvert_commands(list(files), [theme])
        num_cpus = multiprocessing.cpu_count()
        print(f'Using {num_cpus} cores to parallelize the conversion effort')
        command_chunks = [commands[i:i+num_cpus] for i in range(0, len(commands), num_cpus)]
        print(f'Breaking the processing into {len(command_chunks)}')
        for i, command_sequence in enumerate(command_chunks):
            print(f'Processing Chunk {i+1}/{len(command_chunks)}')
            run_in_batches(num_cpus, command_sequence)


main()