
"""
    This file preprocesses Microsoft Malware Classification Challange data
    for machine learning models and further examination
"""

import csv
import os
import pickle

import numpy as np
from scipy.stats import entropy

import utils.config as config
from utils.io import concat_file_path, get_file_size
from utils.io import is_sequence_file, class_of_sample


class Preprocess:
    def __init__(self, bytes_dir, label_file):
        self.bytes_dir = bytes_dir
        self.label_file = label_file

    def bytes_files_list(self):
        return os.listdir(self.bytes_dir)

    """
        Strips .bytes files from binary addresses and lines to make byte sequence
        
        Input file has 8 characters of address in each line, line[9:] takes
        remaining characters 
    """
    def make_1d_vector(self, file, file_class):
        new_file = '{}{}{}_{}.{}'.format(self.bytes_dir, config.SEPERATOR,
                                         file_class, file.split('.')[0], config.SEQUENCE_FILE_EXTENSION)

        # Skip if file already exists
        if os.path.isfile(new_file):
            return

        n_file = open(new_file, 'w')
        with open('{}{}{}'.format(self.bytes_dir, config.SEPERATOR, file)) as o_file:
            for line in o_file:
                n_file.write(line[9:].rstrip())
                n_file.write(' ')
                
        n_file.close()

    # Makes sequence files using make_1d_vector(*.bytes)
    def make_sequence_files(self, delete_bytes_files):
        with open(self.label_file, 'r') as labels:
            reader = csv.reader(labels)
            class_dict = {rows[0]: rows[1] for rows in reader}

        for file in self.bytes_files_list():
            name, extension = file.split('.')

            if extension == config.BYTE_FILE_EXTENSION:
                self.make_1d_vector(file, class_dict[name])
                if delete_bytes_files:
                    os.remove(concat_file_path(self.bytes_dir, file))


# BoW feature extraction for byte files
class BagOfWords:
    def __init__(self, bytes_dir, file):
        self.file = concat_file_path(bytes_dir, file)
        self.byte_frequency = [0] * 256
        self.probability = []
        self.extracted = False

    def extract(self):
        with open(self.file, 'r') as f:
            for byte in f.readline().split(' '):
                try:
                    ix = int(byte, 16)
                    self.byte_frequency[ix] += 1
                except:
                    pass

    def prob(self):
        if not self.extracted:
            self.extract()

        byte_count = sum(self.byte_frequency)
        if byte_count == 0:
            self.probability = self.byte_frequency
        else:
            self.probability = [i / byte_count for i in self.byte_frequency]

        return self.probability

    def entropy(self):
        return np.nan_to_num(entropy(self.probability, base=2 ** 8))


# Preprocessing function
def preprocess():
    if os.path.isfile(config.PICKLE_X1) and os.path.isfile(config.PICKLE_X2) and os.path.isfile(config.PICKLE_y):
        # If pickle files exist already
        with open(config.PICKLE_X1, 'rb') as f:
            X1 = pickle.load(f)

        with open(config.PICKLE_X2, 'rb') as f:
            X2 = pickle.load(f)

        with open(config.PICKLE_y, 'rb') as f:
            y = pickle.load(f)

    else:
        # If there are no pickle files
        p = Preprocess(config.BYTES_DIR, config.LABEL_FILE)
        p.make_sequence_files(delete_bytes_files=True)

        X1 = []
        X2 = []
        y = []
        for sample in os.listdir(config.BYTES_DIR):
            if is_sequence_file(sample):
                # Extract byte probability distribution and add to samples
                bow = BagOfWords(config.BYTES_DIR, sample)
                X1.append(bow.prob())
                # Append class to class vector
                y.append(class_of_sample(sample))

                # Make entropy-file size vector and add to data matrix
                X2.append([bow.entropy(), get_file_size(concat_file_path(config.BYTES_DIR, sample))])

        # Make pickle files
        with open(config.PICKLE_X1, 'wb') as f:
            pickle.dump(X1, f)

        with open(config.PICKLE_X2, 'wb') as f:
            pickle.dump(X2, f)

        with open(config.PICKLE_y, 'wb') as f:
            pickle.dump(y, f)

    return X1, X2, y
