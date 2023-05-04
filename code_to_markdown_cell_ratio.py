import pandas


def main():
    df = pandas.read_csv('nb_processed_cell_html.csv')
    # Group by filename and cellType
    x = df.groupby(['fileNames', 'cellType']).agg(cellType_count=('cellType', 'count'))
    x = x.reset_index()
    # Set index and unstack
    y = x.set_index(['fileNames', 'cellType']).unstack(['cellType']).reset_index()
    y['ratio'] = y['cellType_count']['code'] / y['cellType_count']['markdown']
    y = y.sort_values(by=['ratio'], ascending=False)  # Most code cells and minimum markdown cells

    print(y['ratio'].describe())


main()

