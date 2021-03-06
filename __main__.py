

import random

import numpy as np
from sklearn.model_selection import train_test_split

import utils.config as config
from utils.metrics import show_metrics, show_conf_matrix, dtree_viz
from utils.models import DecisionTree, RandomForest, KNeighbours, ArtificialNeuralNetwork, XGBoost, \
    Results, VotingClassifier
from utils.preprocessing import preprocess

# Eliminate randomness
np.random.seed(1337)
random.seed(1337)

# Take sequence file as a BoW of bytes and make a probability distribution from that
X1, X2, y = preprocess()

# Cast lists to numpy array
X1 = np.array(X1)
X2 = np.array(X2)
y = np.array(y)

# Split train and test data
X1_train, X1_test, X2_train, X2_test, y_train, y_test = train_test_split(X1, X2, y,
                                                                         test_size=config.TEST_SIZE)

# Make models and train
models_probability = {'dt': DecisionTree, 'rf': RandomForest, 'knn': KNeighbours, 'ann': ArtificialNeuralNetwork,
                      'xgb': XGBoost}
results_probability = {}

for name, model in models_probability.items():
    clf = model(X1_train, y_train)
    y_pred = clf.predict(X1_test)
    proba = clf.predict_proba(X1_test)
    results = Results(model.__name__, y_pred, proba)

    # Evaluate results
    show_metrics(results, y_test, truncate=False)
    show_conf_matrix(results, y_test)

    # Save for voting classifier
    results_probability.update({name: results})

    # Visualize decision tree
    if name == 'dt':
        dtree_viz(clf.best_estimator_, 'prob_dt.png')

models_file_properties = {'dt': DecisionTree, 'rf': RandomForest, 'xgb': XGBoost}
results_file_properties = {}

for name, model in models_file_properties.items():
    clf = model(X2_train, y_train)
    y_pred = clf.predict(X2_test)
    proba = clf.predict_proba(X2_test)
    results = Results(model.__name__, y_pred, proba)

    show_metrics(results, y_test, truncate=False)
    show_conf_matrix(results, y_test)

    results_file_properties.update({name: results})

    if name == 'dt':
        dtree_viz(clf.best_estimator_, 'file_dt.png')

weights = [0.32255784, 0.98224021, 0.21065342, 0.57632579, 0.9836862, 0.22180763, 0.34818698, 0.45107591]

votingClassifier = VotingClassifier()
votingClassifier.addClassifier(results_probability['dt'], weights[0])
votingClassifier.addClassifier(results_probability['rf'], weights[1])
votingClassifier.addClassifier(results_probability['knn'], weights[2])
votingClassifier.addClassifier(results_probability['ann'], weights[3])
votingClassifier.addClassifier(results_probability['xgb'], weights[4])
votingClassifier.addClassifier(results_file_properties['dt'], weights[5])
votingClassifier.addClassifier(results_file_properties['rf'], weights[6])
votingClassifier.addClassifier(results_file_properties['xgb'], weights[7])
clf = votingClassifier.calculateOverallResult()

accuracy = show_metrics(clf, y_test)
