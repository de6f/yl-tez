

"""
    This file preprocesses Microsoft Malware Classification Challange data
    for machine learning models and further examination
"""


import os
import csv

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
        new_file = '{}\\{}_{}.seq'.format(self.bytes_dir,
                                          file_class, file.split('.')[0])
        
        # Skip if file already exists
        if os.path.isfile(new_file):
            return
        
        n_file = open(new_file, 'w')
        with open('{}\\{}'.format(self.bytes_dir, file)) as o_file:
            for line in o_file:
                n_file.write(line[9:].rstrip())
                n_file.write(' ')
                
        n_file.close()    
    
    
    """
        Makes .seq files using make_1d_vector(*.bytes)
    """
    
    def make_sequence_files(self):
        with open(self.label_file, 'r') as labels:
            reader = csv.reader(labels)
            class_dict = {rows[0]:rows[1] for rows in reader}
        
        for file in self.bytes_files_list():
            name, extension = file.split('.')
            
            if extension == 'bytes':
                self.make_1d_vector(file, class_dict[name])
            
            
    def __call__(self):
        self.make_sequence_files()
            
        
"""
    BoW feature extraction for byte files
"""
        
class bag_of_words:
    def __init__(self, bytes_dir, file):
        self.file = '{}\\{}'.format(bytes_dir, file)
        self.byte_frequency = [0] * 256
        self.hist = []
        
    def extract(self):
        with open(self.file, 'r') as f:
            for byte in f.readline().split(' '):
                try:
                    ix = int(byte, 16)
                except:
                    pass
                
                self.byte_frequency[ix] += 1
                
                
    def histogram(self):
        byte_count = sum(self.byte_frequency)
        self.hist = [i / byte_count for i in self.byte_frequency]
        
    def __call__(self):
        self.extract()
        self.histogram()
        
        return self.hist
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        