
import os

import utils.config as config


def is_sequence_file(f):
    return f.endswith(config.SEQUENCE_FILE_EXTENSION)


def class_of_sample(f_without_path):
    return int(f_without_path[0])


def concat_file_path(dir_path, file_name):
    return "{}{}{}".format(dir_path, config.SEPERATOR, file_name)


def get_file_size(f):
    return os.stat(f).st_size
