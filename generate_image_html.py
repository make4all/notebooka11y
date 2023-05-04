import os
import glob
import numpy


def main():
    files = glob.glob('data-100k/base64Images/*.png')
    file_to_file_size = {}
    for f in files:
        file_to_file_size[f] = os.path.getsize(f)

    file_sizes = list(file_to_file_size.values())


    for i in [10, 25, 50, 75, 90, 95, 99, 100]:
        print(i, numpy.percentile(file_sizes, i))




main()


