import pandas
import json
import numpy


df = pandas.read_csv('bak/nb_processed_cell_html.csv', converters={'_table_metadata': json.loads})
print(df)

def process_r_c_tuples(item):
    s = []
    for d in item:
        s.append((d['num_rows'], d['num_columns']))
    return s


df['table_metadata'] = df['_table_metadata'].apply(lambda x: process_r_c_tuples(x))
print(df)

gdf = df.groupby(['fileNames']).agg({'table_metadata': lambda x: list(x)})

def flatten(arr):
    r = []
    for i in arr:
        for x in i:
            r.append(x)
    return r

gdf['table_metadata'] = gdf['table_metadata'].apply(lambda r: flatten(r))
gdf['num_tables'] = gdf['table_metadata'].apply(lambda x: len(x))

print(gdf)

gdf = gdf[gdf['num_tables'] > 0]
print(gdf.shape)


def cdf(data, sort_needed=True):
    n = len(data)
    x = data
    if sort_needed:
        x = numpy.sort(data)
    y = numpy.arange(1, n+1) / n
    return x, y


import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=1, ncols=1)
num_tables_count = gdf['num_tables'].tolist()
X, Y = cdf(num_tables_count)
for p in [25, 50, 75, 90, 95, 99]:
    print('Tables: ' + str(numpy.percentile(X, p)))
ax.plot(X, Y)
ax.set_xlabel('Number of Tables Per Notebook')
ax.set_ylabel('CDF Of Number of Tables Per Notebook')
ax.set_xscale('log')
plt.savefig('table_cdf.pdf', bbox_inches='tight')

fig, ax = plt.subplots(nrows=1, ncols=1)
rows = []
columns = []
row_col_details = []
elements = gdf['table_metadata'].tolist()
for d in elements:
    for pair in d:
        row_col_details.append(pair)
        rows.append(pair[0])
        columns.append(pair[1])

rows_X, rows_Y = cdf(rows)
cols_X, cols_Y = cdf(columns)
for p in [25, 50, 75, 90, 95, 99]:
    print('Rows : ' + str(numpy.percentile(rows_X, p)))
    print('Cols : ' + str(numpy.percentile(cols_X, p)))
ax.plot(rows_X, rows_Y, label='Rows')
ax.plot(cols_X, cols_Y, label='Columns')
ax.legend()
ax.set_xscale('log')
ax.set_xlabel('Number of Rows/Columns in a Table')
ax.set_ylabel('CDF')
plt.savefig('row_cols_cdf.pdf', bbox_inches='tight')


dfcols = ['Row', 'Column']
dfrows = []
for pair in row_col_details:
    dfrows.append([pair[0], pair[1]])

rcdf = pandas.DataFrame(data=dfrows, columns=dfcols)

import seaborn as sns
fig, ax = plt.subplots(nrows=1, ncols=1)
sns.lmplot(data=rcdf, x="Row", y="Column")
ax.set_xscale('log')
plt.savefig('table_scatter.pdf', bbox_inches='tight')

