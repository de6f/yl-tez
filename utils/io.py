import utils.config as config

def isSequenceFile(f):
    return f.endswith(config.SEQUENCE_FILE_EXTENSION)

def classOfSample(f_without_path):
    return int(f_without_path[0])
