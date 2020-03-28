

import utils.config as config

"""
    Preprocessing
"""
from utils.preprocessing import preprocess

p = preprocess(config.BYTES_DIR, config.LABEL_FILE)
p.make_sequence_files()

"""
    Take sequence file as a BoW of bytes and make a probability histogram from that
"""
import os
from utils.preprocessing import bag_of_words
from utils.io import isSequenceFile, classOfSample

X = []
y = []

for sample in os.listdir(config.BYTES_DIR):
    if isSequenceFile(sample):
        # Extract byte probability distribution and add to samples
        bow = bag_of_words(config.BYTES_DIR, sample)
        X.append(bow.hist())
        # Append class to class vector
        y.append(classOfSample(sample))

"""
    Visualize class histograms
"""
from utils.visualization import showHistogramForClasses

showHistogramForClasses(X, y)

"""
    Decision tree 
"""


def DecisionTree(X, y):
    from sklearn import tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf
