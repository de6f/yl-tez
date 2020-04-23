import utils.config as config

"""
    Eleminate randomness
"""
import numpy as np
np.random.seed(1337)

import random
random.seed(1337)

"""
    Take sequence file as a BoW of bytes and make a probability distribution from that
"""
from utils.preprocessing import preprocess

X1, X2, y = preprocess()

"""
    Cast lists to numpy array
"""
import numpy as np

X1 = np.array(X1)
X2 = np.array(X2)
y = np.array(y)

"""
    Split train and test data
"""
from sklearn.model_selection import train_test_split

X1_train, X1_test, X2_train, X2_test, y_train, y_test = train_test_split(X1, X2, y,
                                                                         test_size=config.TEST_SIZE)

"""
    Make models and train
"""
from utils.models import DecisionTree, RandomForest, KNeighbours, ArtificialNeuralNetwork, XGBoost
from utils.metrics import show_metrics
from utils.models import Results

models_probability = {'dt': DecisionTree, 'rf': RandomForest, 'knn': KNeighbours, 'ann': ArtificialNeuralNetwork,
                      'xgb': XGBoost}
results_probability = {}

for name, model in models_probability.items():
    clf = model(X1_train, y_train)
    y_pred = clf.predict(X1_test)
    proba = clf.predict_proba(X1_test)
    results = Results(model.__name__, y_pred, proba)

    # Evaluate results
    show_metrics(results, y_test)
    """
    show_conf_matrix(model, y_test)
    """

    # Save for voting classifier
    results_probability.update({name: results})

models_file_properties = {'dt': DecisionTree, 'rf': RandomForest, 'xgb': XGBoost}
results_file_properties = {}

for name, model in models_file_properties.items():
    clf = model(X2_train, y_train)
    y_pred = clf.predict(X2_test)
    proba = clf.predict_proba(X2_test)
    results = Results(model.__name__, y_pred, proba)

    show_metrics(results, y_test)
    """
    show_conf_matrix(results, y_test)
    """

    results_file_properties.update({name: results})

from utils.models import VotingClassifier

votingClassifier = VotingClassifier()
votingClassifier.addClassifier(result_probability['rf'], 0.9)
votingClassifier.addClassifier(result_probability['xgb'], 0.9)
votingClassifier.addClassifier(results_file_properties['dt'], 0.1)
votingClassifier.addClassifier(results_file_properties['rf'], 0.2)
votingClassifier.addClassifier(results_file_properties['xgb'], 0.1)
clf = votingClassifier.calculateOverallResult()

show_metrics(clf, y_test)
