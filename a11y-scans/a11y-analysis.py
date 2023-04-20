from collections import defaultdict

import pandas
import swifter
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

def read_detailed_information(filepath='../a11y-detailed-result.csv'):
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

def analyseErrors(df):
    
    # print(df.columns)
    # print(df.shape)
    # print(df.describe())
    # sample
    # print(df.sample(3))
    # group by runner
    # print("group by runner")
    # print(df.groupby('Runner').head())#.describe().head())
    # print(df.groupby('Standard').count().sort_values(by='Theme', ascending=False))
    # drop rows where runner is not 'axe'. just for tessting
    # axedf = df[df['Runner'] == 'axe']
    # drop the runner column
    print(f"dropping id and selector from df of shape {df.shape}")
    df = df.drop(columns=[ 'Selector','ID'])
    # print the columns
    # print(axedf.columns)
    # print(axedf.sample(3))
    # drop everything where type is not error
    # axedf = axedf[axedf['Type'] == 'error']
# group by theme. count notebooks. filter where count <6
    nbagg = df.swifter.groupby('Notebook').swifter.agg({'Theme': 'nunique'}).reset_index()
    nbagg = nbagg[nbagg['Theme'] == 6]
    nbset = nbagg['Notebook']
    df = pandas.merge(df, nbset, on=['Notebook'], how='inner')
    #df=df.groupby('Theme').filter(lambda x: x['Notebook'].count() >= 6)
    # group by theme and print counts
    

    # count errors that have tables and print them
    # print(f"Number of errors related to tables: {df['DetailCode'].str.contains('table').sum()}")
    # group by theme and print counts of detailedCodes containing tables
    # print("group by theme and print counts of detailedCodes containing tables")
    # print(f"{df.groupby('Theme')['DetailCode'].apply(lambda x: x.str.contains('table').sum())}")
    # # group by type and print counts of detail code containing tables
    # print("group by type and print counts of detail code containing tables")
    # print(f"{axedf.groupby('Type')['DetailCode'].apply(lambda x: x.str.contains('table').sum())}")
    # group by theme and drop values where notebook is not present in all themes
    # df2 = df.groupby('Theme').filter(lambda x: x['Notebook'].nunique() == 1)
    
    # print("group by theme, check for detailCode containing table, group by detailCode and print counts")
    # print(f"{axedf[axedf['DetailCode'].str.contains('table')].groupby('Theme')['DetailCode'].value_counts()}")
    # group by theme and detailCode and print counts for each detail code in each theme
    # print("group by theme and detailCode and print counts for each detail code in each theme")
    # print(f"{df.groupby(['Theme', 'DetailCode'])['DetailCode'].count()}")
# count unique detailCodes, and store detailCode, runner, count in a new df
    df = df.swifter.groupby(['DetailCode', 'Runner','Type','Theme'])['DetailCode'].swifter.count().reset_index(name='count')
    # sorting output for easy screen readability
    # sort by type, and decreasing order of count
    df = df.swifter.sort_values(by=['Type','Runner','count'], ascending=[True,True, False])
    df.to_csv('a11y-error-warning-notice-counts.csv', index=False)
    # group by DetailCode and filter for groups where there are lessthan 6 unique themes in each group
    df.swifter.groupby('DetailCode').swifter.filter(lambda x: x['Theme'].swifter.nunique() < 6).to_csv('a11y-error-warning-notice-counts-summary.csv', index=False)
    # print(f"a summary of df3 is {df3.shape} ")
    # print(df3)
    
    # group by detailCode, filter for entries where number of unique counts is >1
    df.swifter.groupby('DetailCode').filter(lambda x: x['count'].nunique() > 1).to_csv('a11y-error-warning-notice-counts-diffs.csv', index=False)
    # filter for type to be error
    # df.swifter.groupby('DetailCode').swifter.filter(lambda x: x['count'].swifter.nunique() > 1).loc]
    # print(df4.shape)
    # print(df4.sample(5))
    # df4.to_csv('a11y-error-counts-diffs.csv', index=False)
    # print(f"sample of df2 is {df2.sample() }"    )

    
    # print the list of unique detail codes
    # print(f"list of unique detail codes: {df['DetailCode'].unique()}")

    # group by theme and check if every filename is in each theme
    # group = axedf.groupby('Theme')
    # check if each group has the same number of filenames
    # print(group.apply(lambda x: x['Notebook'].nunique()))
    # split each group into its own dataframe
    # darkDF = group.get_group('dark')
    # darculaDF = group.get_group('darcula')
    # materialDarkerDf = group.get_group('material-darker')
    # solarizedDF = group.get_group('solarized')
    # lightDF = group.get_group('light')
    # HhorizonDF = group.get_group('horizon')
    # join so that data is uniform. that is, we have results for a notebook in each template
    
    # print(jointdf.shape)
    # print(jointdf.describe())
    # print("a sample of these errors are")
    # print(axedf[axedf['DetailCode'].str.contains('table')].sample(20))

    # print(axedf.sample(20)) 
    # print counts of errors related to tables
    


if __name__ == '__main__':
    # df = read_aggregate_information()
    ddf = read_detailed_information()
    ddf = ddf.sample(n=500)
    analyseErrors(ddf)
    # plot_aggregate_errors_and_warnings(df)

