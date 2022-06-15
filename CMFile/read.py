import os
import sys


def read_file_as_str(file_path):
    # exist?

    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    with open(file_path) as f:
        all_the_text = f.read()
    # print type(all_the_text)
    return all_the_text
