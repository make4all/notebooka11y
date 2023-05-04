import pandas


def main():
    df = pandas.read_csv('nb_processed_cell_html.csv')
    df = df[['fileNames', 'cell_seq_num', 'cellType', '_has_output', '_output_contains_graphics', '_output_contains_tables', '_has_heading', 'has_tables', 'has_math']]

    query_df = df[(df['cellType'] == 'code') & (df['_has_output'] == True) & (df['_output_contains_graphics'] == True)]

    markdown_before = []
    markdown_after = []

    before_contains_heading = []
    after_contains_heading = []
    before_contains_tables = []
    after_contains_tables = []
    before_contains_math = []
    after_contains_math = []

    for index, row in query_df.iterrows():
        if index % 1000:
            print(f'Processing {index}/{len(query_df)} rows.')
        cell_sequence_number = row['cell_seq_num']
        filename = row['fileNames']
        before_fdf = df[(df['fileNames'] == filename) & (df['cell_seq_num'] == cell_sequence_number - 1) & (df['cellType'] == 'markdown')]
        if len(before_fdf) == 1:
            markdown_before.append(True)

            has_heading = before_fdf['_has_heading']
            has_table = before_fdf['has_tables']
            has_math = before_fdf['has_math']

            before_contains_heading.append(has_heading)
            before_contains_tables.append(has_table)
            before_contains_math.append(has_math)
        else:
            markdown_before.append(False)
            before_contains_heading.append(False)
            before_contains_tables.append(False)
            before_contains_math.append(False)

        after_fdf = df[(df['fileNames'] == filename) & (df['cell_seq_num'] == cell_sequence_number + 1) & (df['cellType'] == 'markdown')]
        if len(after_fdf) == 1:
            markdown_after.append(True)

            has_heading = after_fdf['_has_heading']
            has_table = after_fdf['has_tables']
            has_math = after_fdf['has_math']

            after_contains_heading.append(has_heading)
            after_contains_tables.append(has_table)
            after_contains_math.append(has_math)
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

    query_df.to_csv('code_markdown_before_after_with_metadata.csv', header=True, index=False)


main()

