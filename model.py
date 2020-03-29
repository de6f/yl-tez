

import utils.config as config

"""
    Preprocessing
"""
from utils.preprocessing import Preprocess

p = Preprocess(config.BYTES_DIR, config.LABEL_FILE)
p.make_sequence_files(delete_bytes_files=True)

"""
    Take sequence file as a BoW of bytes and make a probability distribution from that
"""
import os
from utils.preprocessing import BagOfWords
from utils.io import isSequenceFile, classOfSample

X = []
y = []

for sample in os.listdir(config.BYTES_DIR):
    if isSequenceFile(sample):
        # Extract byte probability distribution and add to samples
        bow = BagOfWords(config.BYTES_DIR, sample)
        X.append(bow.hist())
        # Append class to class vector
        y.append(classOfSample(sample))

"""
    Split train and test data
"""
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.TEST_SIZE)

"""
    Visualize class histograms
"""
from utils.visualization import VisualizeClasses

viz = VisualizeClasses(X, y)
viz.compute_class_avg()
viz.show_class_histogram()

"""
    Decision tree 
"""
def DecisionTree(X, y):
    from sklearn import tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf
