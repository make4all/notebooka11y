import pandas
import json


def main():
    df = pandas.read_csv('nb_processed_cell_html.csv')
    print('Processing ALT')
    df['alt-str'] = df['alt_text'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H1')
    df['h1-str'] = df['h1_texts'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H2')
    df['h2-str'] = df['h2_texts'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H3')
    df['h3-str'] = df['h3_texts'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H4')
    df['h4-str'] = df['h4_texts'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H5')
    df['h5-str'] = df['h5_texts'].apply(lambda r: " ".join(json.loads(r)))
    print('Processing H6')
    df['h6-str'] = df['h6_texts'].apply(lambda r: " ".join(json.loads(r)))

    print('Starting to Filter. ...')
    # Filter the texts out
    alt_str_list = df['alt-str'].tolist()
    alt_str_list = list(filter(None, alt_str_list))

    h1_str_list = df['h1-str'].tolist()
    h1_str_list = list(filter(None, h1_str_list))

    h2_str_list = df['h2-str'].tolist()
    h2_str_list = list(filter(None, h2_str_list))

    h3_str_list = df['h3-str'].tolist()
    h3_str_list = list(filter(None, h3_str_list))

    h4_str_list = df['h4-str'].tolist()
    h4_str_list = list(filter(None, h4_str_list))

    h5_str_list = df['h5-str'].tolist()
    h5_str_list = list(filter(None, h5_str_list))

    h6_str_list = df['h6-str'].tolist()
    h6_str_list = list(filter(None, h6_str_list))

    disk_writes = [
            (h1_str_list, 'texts/h1.txt'),
            (h2_str_list, 'texts/h2.txt'),
            (h3_str_list, 'texts/h3.txt'),
            (h4_str_list, 'texts/h4.txt'),
            (h5_str_list, 'texts/h5.txt'),
            (h6_str_list, 'texts/h6.txt'),
            (alt_str_list, 'texts/alt.txt')
        ]

    for data, filename in disk_writes:
        print(f'Writing to disk ... {filename}')
        text = " ".join(data)
        with open(filename, 'w') as f:
            f.write(text)


main()
