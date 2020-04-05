"""
    Model parameters
"""
TEST_SIZE = 0.5

"""
    Files and directories for data
"""
BYTES_DIR = './bytes'
LABEL_FILE = './veri/trainLabels.csv'
PICKLE_X = './bytes/data_bow.pickle'
PICKLE_y = './bytes/labels_bow.pickle'

"""
    Data properties
"""
CLASSES = range(1, 10)
CLASS_COUNT = len(CLASSES)

"""
    Filesystem access constants 
"""
SEPERATOR = '/'
SEQUENCE_FILE_EXTENSION = 'seq'
BYTE_FILE_EXTENSION = 'bytes'