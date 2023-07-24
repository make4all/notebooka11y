from pathlib import Path

LATEX_VARIABLE_OUT_DIR = 'plot_out/tex/'
LATEX_VARIABLE_OUT_FILE = f'{LATEX_VARIABLE_OUT_DIR}variables.tex'

Path(LATEX_VARIABLE_OUT_DIR).mkdir(parents=True, exist_ok=True)


def write_variable_to_tex(variable_string, value):
    with open(LATEX_VARIABLE_OUT_FILE, 'a') as f:
        text = r"\newcommand{" + variable_string + "{" + value + "\n}}" + "\n"
        f.write(text)
    f.close()
