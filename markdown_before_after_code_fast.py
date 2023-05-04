import pandas
import os
import pandas


def main():
    df = pandas.read_csv('nb_processed_cell_html.csv')
    df = df[['fileNames', 'cell_seq_num', 'cellType', '_has_output', '_output_contains_graphics', '_output_contains_tables', '_has_heading', 'has_tables', 'has_math']]
    df = df.sort_values(by=['fileNames', 'cell_seq_num'], ascending=True)
    print(f'Size of Dataframe: {df.shape}')

    query_df = df[(df['cellType'] == 'code') & (df['_has_output'] == True) & (df['_output_contains_graphics'] == True)]
    print(f'Size of Query Dataframe: {query_df.shape}')

    markdown_before = []
    markdown_after = []

    before_contains_heading = []
    after_contains_heading = []
    before_contains_tables = []
    after_contains_tables = []
    before_contains_math = []
    after_contains_math = []

    lookup_table = {}

    print('Pass 1 -- Creating the in-memory table')

    pass1_counter = 0
    for index, row in df.iterrows():
        pass1_counter += 1
        if pass1_counter % 100000 == 0:
            print(f'\tPass 1- Processed {pass1_counter} rows')
        filename = row['fileNames']
        sequence_number = int(row['cell_seq_num'])
        if filename not in lookup_table:
            lookup_table[filename] = {}
        if sequence_number not in lookup_table[filename]:
            lookup_table[filename][sequence_number] = {}

        cell_type = row['cellType']
        has_output = row['_has_output']
        output_contains_graphics = row['_output_contains_graphics']
        output_contains_tables = row['_output_contains_tables']
        has_heading = row['_has_heading']
        has_tables = row['has_tables']
        has_math = row['has_math']

        lookup_table[filename][sequence_number]['cellType'] = cell_type
        lookup_table[filename][sequence_number]['has_output'] = has_output
        lookup_table[filename][sequence_number]['output_contains_graphics'] = output_contains_graphics
        lookup_table[filename][sequence_number]['output_contains_tables'] = output_contains_tables
        lookup_table[filename][sequence_number]['has_heading'] = has_heading
        lookup_table[filename][sequence_number]['has_tables'] = has_tables
        lookup_table[filename][sequence_number]['has_math'] = has_math

    print('Pass 2 -- Performing the lookups for before and after')

    counter = 0
    for index, row in query_df.iterrows():
        counter += 1
        if counter % 10000 == 0:
            print(f'\tPass 2 - Processed {counter} rows')
        filename = row['fileNames']
        sequence_number = int(row['cell_seq_num'])
        pre_check = sequence_number - 1
        post_check = sequence_number + 1

        if pre_check in lookup_table[filename]:
            r = lookup_table[filename][pre_check]
            markdown_before.append(r['cellType'] == 'markdown')
            before_contains_heading.append(r['has_heading'])
            before_contains_tables.append(r['has_tables'])
            before_contains_math.append(r['has_math'])
        else:
            markdown_before.append(False)
            before_contains_heading.append(False)
            before_contains_tables.append(False)
            before_contains_math.append(False)

        if post_check in lookup_table[filename]:
            r = lookup_table[filename][post_check]
            markdown_after.append(r['cellType'] == 'markdown')
            after_contains_heading.append(r['has_heading'])
            after_contains_tables.append(r['has_tables'])
            after_contains_math.append(r['has_math'])
        else:
            markdown_after.append(False)
            after_contains_heading.append(False)
            after_contains_tables.append(False)
            after_contains_math.append(False)

    query_df['markdown_before'] = markdown_before
    query_df['markdown_after'] = markdown_after

    query_df['before_contains_heading'] = before_contains_heading
    query_df['before_contains_tables'] = before_contains_tables
    query_df['before_contains_math'] = before_contains_math

    query_df['after_contains_heading'] = after_contains_heading
    query_df['after_contains_tables'] = after_contains_tables
    query_df['after_contains_math'] = after_contains_math

    query_df.to_csv('code_markdown_before_after_with_metadata_fast.csv', header=True, index=False)


main()

