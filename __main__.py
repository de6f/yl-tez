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

models_probability = {'dt': DecisionTree, 'rf': RandomForest, 'knn': KNeighbours, 'ann': ArtificialNeuralNetwork,
                      'xgb': XGBoost}

for model in models_probability.values():
    clf = model(X1_train, y_train)
    model.__results__ = clf.predict(X1_test)
    model.__proba__ = clf.predict_proba(X1_test)

    # Evaluate results
    show_metrics(model, y_test)
    """
    show_conf_matrix(model, y_test)
    """

models_file_properties = {'dt': DecisionTree, 'rf': RandomForest, 'xgb': XGBoost}
results_file_properties = {'dt', }

for model in models_file_properties.values():
    clf = model(X2_train, y_train)
    model.__results__ = clf.predict(X2_test)
    model.__proba__ = clf.predict_proba(X2_test)

    # Evaluate results

    show_metrics(model, y_test)
    """
    show_conf_matrix(model, y_test)
    """

from utils.models import VotingClassifier

votingClassifier = VotingClassifier()
votingClassifier.addClassifier(models_probability['rf'])
# votingClassifier.addClassifier(models_probability['xgb'])
# votingClassifier.addClassifier(models_file_properties['rf'])
clf = votingClassifier.calculateOverallResult()

show_metrics(clf, y_test)
