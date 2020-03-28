"""
    This file preprocesses Microsoft Malware Classification Challange data
    for machine learning models and further examination
"""

import csv
import os

import utils.config as config


class preprocess:
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

    """
        Makes sequence files using make_1d_vector(*.bytes)
    """
    def make_sequence_files(self):
        with open(self.label_file, 'r') as labels:
            reader = csv.reader(labels)
            class_dict = {rows[0]:rows[1] for rows in reader}
        
        for file in self.bytes_files_list():
            name, extension = file.split('.')

            if extension == config.BYTE_FILE_EXTENSION:
                self.make_1d_vector(file, class_dict[name])
        
"""
    BoW feature extraction for byte files
"""
class bag_of_words:
    def __init__(self, bytes_dir, file):
        self.file = '{}{}{}'.format(bytes_dir, config.SEPERATOR, file)
        self.byte_frequency = [0] * 256
        self.histogram = []
        self.extracted = False

    def extract(self):
        with open(self.file, 'r') as f:
            for byte in f.readline().split(' '):
                try:
                    ix = int(byte, 16)
                except:
                    pass

                self.byte_frequency[ix] += 1

    def hist(self):
        if not self.extracted:
            self.extract()

        byte_count = sum(self.byte_frequency)
        self.histogram = [i / byte_count for i in self.byte_frequency]

        return self.histogram

    def __call__(self):
        return self.hist
