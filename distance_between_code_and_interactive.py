import pandas
from collections import defaultdict

df = pandas.read_csv('nb_processed_cell_html.csv')

notebook_files = list(set(df['fileNames'].tolist()))

distance_to_first_interactive_heading_or_table = defaultdict(list)

for filename in notebook_files:
    sel_df = df[df['fileNames'] == filename]
    for index, row in sel_df.iterrows():
        seq_num = row['cell_seq_num']
        cell_type = row['cellType']
        has_heading = row['_has_heading']
        has_tables = row['has_tables']
        if has_heading or has_tables:
            if has_tables:
                distance_to_first_interactive_heading_or_table[filename].append(['Table', seq_num, None])
            if has_heading:
                min_heading = None
                is_h1 = row['_num_h1']
                is_h2 = row['_num_h2']
                is_h3 = row['_num_h3']
                is_h4 = row['_num_h4']
                is_h5 = row['_num_h5']
                is_h6 = row['_num_h6']
                if is_h1 > 0:
                    min_heading = 1
                if is_h2 > 0:
                    min_heading = 2
                if is_h3 > 0:
                    min_heading = 3
                if is_h4 > 0:
                    min_heading = 4
                if is_h5 > 0:
                    min_heading = 5
                if is_h6 > 0:
                    min_heading = 6
                distance_to_first_interactive_heading_or_table[filename].append(['Heading', seq_num, min_heading])
            break

rows = []
for filename, sequences in distance_to_first_interactive_heading_or_table.items():
    row = [None, None, None, None, None, None, None]
    row[0] = filename
    for seq in sequences:
        if seq[0] == 'Heading':
            row[1] = seq[0]
            seq_num = seq[1]
            heading_level = seq[2]

            row[1] = seq[0]
            row[2] = seq_num
            row[3] = heading_level
        if seq[0] == 'Table':
            seq_num = seq[1]
            table_level = seq[2]

            row[4] = seq[0]
            row[5] = seq_num
            row[6] = table_level

    rows.append(row)

rdf = pandas.DataFrame(data=rows, columns=['Filename', 'H', 'SequenceNumber', 'HLevel', 'T', 'TSequenceNumber', 'TDetail'])
rdf.to_csv('nb_first_interactive_cell.csv', header=True, index=False)

