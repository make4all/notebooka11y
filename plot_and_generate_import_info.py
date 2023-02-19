import pandas
import json
from collections import Counter

df = pandas.read_csv('nb_processed.csv')

libraries = []
functions_called = []

for index, row in df.iterrows():
    import_list = json.loads(row['imports'])
    for imported_line in import_list:
        imported_line = imported_line.lstrip()
        split_elements = imported_line.split()
        if len(split_elements) == 1:
            libraries.append(split_elements[0])
        else:
            lib, func = split_elements
            libraries.append(lib)
            functions_called.append(lib + '.' + func)

library_counter = Counter(libraries).most_common()

lib_df_rows = []
for libname, count in library_counter:
    lib_df_rows.append([libname, count])
libdf = pandas.DataFrame(data=lib_df_rows, columns=['module', 'count'])
libdf.to_csv('module_import_counts.csv', header=True, index=False)

import altair as alt
from altair_saver import save


bars = alt.Chart(libdf).mark_bar().encode(
    y=alt.Y('module:N', sort='-x'),
    x=alt.X('count')
)

bars.save('model/summary-1k/modules-imported.html')

