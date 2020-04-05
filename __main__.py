

import utils.config as config

"""
    Take sequence file as a BoW of bytes and make a probability distribution from that
"""
import os
import pickle

from utils.preprocessing import BagOfWords
from utils.io import isSequenceFile, classOfSample

X = []
y = []

if os.path.isfile(config.PICKLE_X) and os.path.isfile(config.PICKLE_y):
    # If pickle files exist already
    with open(config.PICKLE_X, 'rb') as f:
        X = pickle.load(f)

    with open(config.PICKLE_y, 'rb') as f:
        y = pickle.load(f)

else:
    # If there are no pickle files
    """
        Preprocessing
    """
    from utils.preprocessing import Preprocess

    p = Preprocess(config.BYTES_DIR, config.LABEL_FILE)
    p.make_sequence_files(delete_bytes_files=True)

    for sample in os.listdir(config.BYTES_DIR):
        if isSequenceFile(sample):
            # Extract byte probability distribution and add to samples
            bow = BagOfWords(config.BYTES_DIR, sample)
            X.append(bow.hist())
            # Append class to class vector
            y.append(classOfSample(sample))

    # Make pickle files
    with open(config.PICKLE_X, 'wb') as f:
        pickle.dump(X, f)

    with open(config.PICKLE_y, 'wb') as f:
        pickle.dump(y, f)

"""
    Cast lists to numpy array
"""
import numpy as np

X = np.array(X)
y = np.array(y)

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
    Make model and train
"""
from utils.models import DecisionTree, RandomForest, KNeighbours, ArtificialNeuralNetwork

dt = DecisionTree(X_train, y_train)
y_pred_dt = dt.predict(X_test)

rf = RandomForest(X_train, y_train)
y_pred_rf = rf.predict(X_test)

knn = KNeighbours(X_train, y_train)
y_pred_knn = knn.predict(X_test)

ann = ArtificialNeuralNetwork(X_train, y_train)
y_pred_ann = ann.predict(X_test)

from sklearn.ensemble import VotingClassifier

estimators = [('dt', dt), ('rf', rf), ('knn', knn)]
ensemble = VotingClassifier(estimators, voting='hard', weights=[0.8, 1, 0.6])

ensemble.fit(X_train, y_train)
y_pred_voting = ensemble.predict(X_test)

from sklearn.metrics import accuracy_score

print("Decision tree accuracy:", accuracy_score(y_test, y_pred_dt))
print("Random forest accuracy:", accuracy_score(y_test, y_pred_rf))
print("k-NearestNeighbour accuracy:", accuracy_score(y_test, y_pred_knn))
print("Neural network accuracy:", accuracy_score(y_test, y_pred_ann))
print("Voting classifier accuracy:", accuracy_score(y_test, y_pred_voting))
