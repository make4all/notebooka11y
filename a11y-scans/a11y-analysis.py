from collections import defaultdict

import pandas
import numpy
import matplotlib.pyplot as plt


def cdf(data, sort_needed=True):
    n = len(data)
    x = data
    if sort_needed:
        x = numpy.sort(data) # sort your data
    y = numpy.arange(1, n + 1) / n # calculate cumulative probability
    return x, y


def read_aggregate_information(filepath='a11y-aggregate-scan.csv'):
    df = pandas.read_csv(filepath)
    return df


def plot_aggregate_errors_and_warnings(df):
    error_results = defaultdict(list)
    warning_results = defaultdict(list)
    for index, row in df.iterrows():
        theme = row['Theme']
        error_count = row['Errors']
        warning_count = row['Warnings']
        error_results[theme].append(error_count)
        warning_results[theme].append(warning_count)

    plot_line_style = {
        'warning': '--',
        'error': '-',
    }
    theme_style = {
        'darcula': '#e77c8d',
        'dark': '#c69255',
        'horizon': '#98a255',
        'light': '#56ad74',
        'material-darker': '#5aa9a2',
        'solarized': '#5ea5c5',
    }
    fig, ax = plt.subplots(nrows=1, ncols=1)
    for plot_type, result_dict in [('error', error_results), ('warning', warning_results)]:
        for theme, arr in result_dict.items():
            theme_color = theme_style[theme]
            line_style = plot_line_style[plot_type]
            X, Y = cdf(arr, sort_needed=True)
            ax.plot(X, Y, label=f'{theme}', linestyle=line_style, color=theme_color)
    ax.set_xlabel('Number of Warnings / Errors related to Accessibility')
    ax.set_ylabel('CDF of warnings/errors')
    ax.set_xscale('log')
    ax.legend()
    plt.savefig('warnings_errors.pdf', bbox_inches='tight')


if __name__ == '__main__':
    df = read_aggregate_information()
    plot_aggregate_errors_and_warnings(df)

