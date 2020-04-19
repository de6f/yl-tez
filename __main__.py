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

X, y = preprocess()

"""
    Cast lists to numpy array
"""
import numpy as np

X = np.array(X)
y = np.array(y)

"""
    Make entropy data
"""
from scipy.stats import entropy

# Suppress warnings
np.seterr(divide='ignore', invalid='ignore')

x_entropy = entropy(X.transpose(), base=2**8)

"""
    Split train and test data
"""
from sklearn.model_selection import train_test_split

X_train, X_test, x_entropy_train, x_entropy_test, y_train, y_test = train_test_split(X, x_entropy, y,
                                                                                     test_size=config.TEST_SIZE)

"""
    Make models and train
"""
from utils.models import DecisionTree, RandomForest, KNeighbours, ArtificialNeuralNetwork, XGBoost
from utils.metrics import show_metrics, show_conf_matrix

models = {'dt': DecisionTree, 'rf': RandomForest, 'knn': KNeighbours, 'ann': ArtificialNeuralNetwork, 'xgb': XGBoost}

for model in models.values():
    model.__results__ = model(X_train, y_train).predict(X_test)

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
