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
from utils.models import DecisionTree, RandomForest, KNeighbours, ArtificialNeuralNetwork, XGBoost, SVM
from utils.metrics import show_metrics, show_conf_matrix

models = {'dt': DecisionTree, 'rf': RandomForest, 'knn': KNeighbours, 'ann': ArtificialNeuralNetwork, 'xgb': XGBoost}

for model in models.values():
    model.__results__ = model(X1_train, y_train).predict(X1_test)

    # Evaluate results
    show_metrics(model, y_test)
    show_conf_matrix(model, y_test)

"""
from sklearn.ensemble import VotingClassifier

estimators = [('dt', dt), ('rf', rf), ('knn', knn)]
ensemble = VotingClassifier(estimators, voting='hard', weights=[0.8, 1, 0.6])

ensemble.fit(X_train, y_train)
y_pred_voting = ensemble.predict(X_test)

print("Voting classifier accuracy:", accuracy_score(y_test, y_pred_voting))
"""

models = {'dt': DecisionTree, 'rf': RandomForest, 'svm': SVM, 'xgb': XGBoost}

for model in models.values():
    model.__results__ = model(X2_train, y_train).predict(X2_test)

    # Evaluate results
    show_metrics(model, y_test)
    show_conf_matrix(model, y_test)
