
from dataclasses import dataclass

import numpy as np
from sklearn.model_selection import GridSearchCV

from utils.config import CLASS_COUNT
from utils.metrics import show_metrics


# Model construction functions
def DecisionTree(X, y):
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    params_dt = {'max_depth': np.arange(1, 21), 'min_samples_leaf': [1, 5, 10, 20, 50, 100]}
    clf = GridSearchCV(clf, params_dt, cv=5)
    clf = clf.fit(X, y)
    return clf


def RandomForest(X, y):
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier()
    params_rf = {'n_estimators': [50, 100, 200]}
    clf = GridSearchCV(clf, params_rf, cv=5)
    clf.fit(X, y)
    return clf


def KNeighbours(X, y):
    from sklearn.neighbors import KNeighborsClassifier
    clf = KNeighborsClassifier()
    params_knn = {'n_neighbors': np.arange(1, 26)}
    clf = GridSearchCV(clf, params_knn, cv=5)
    clf.fit(X, y)
    return clf


def ArtificialNeuralNetwork(X, y):
    from sklearn.neural_network import MLPClassifier
    clf = MLPClassifier(solver='adam', learning_rate_init=0.01, max_iter=500)
    params_ann = {'hidden_layer_sizes': [(50, 25, 25), (50, 25), (25)]}
    clf = GridSearchCV(clf, params_ann, cv=5)
    clf.fit(X, y)
    return clf


def XGBoost(X, y):
    import xgboost as xgb
    clf = xgb.XGBClassifier(random_state=1, learning_rate=0.01)
    clf.fit(X, y)
    return clf


class Results:
    def __init__(self, name, results, probabilities=0):
        self.__name__ = name
        self.__results__ = results
        self.__proba__ = probabilities
        self.__weight__ = 0


class VotingClassifier:
    def __init__(self):
        self.testCount = 0
        self.classifiers = []
        self.weights = []

    def addClassifier(self, results, weight=1):
        # Get test sample count from first model
        if self.classifiers.__len__() == 0:
            self.testCount = len(results.__results__)

        results.__weight__ = weight
        self.classifiers.append(results)

    def calculateOverallResult(self):
        voteMatrix = []

        for i in range(self.testCount):
            classVotes = np.zeros(CLASS_COUNT)
            for clf in self.classifiers:
                classVotes += clf.__proba__[i] * clf.__weight__

            voteMatrix.append(classVotes)

        overallResult = np.argmax(voteMatrix, axis=1) + 1
        return Results('VotingClassifier', overallResult)


def find_optimal_weights(results_probability, results_file_properties, y_test, size=5000):
    weight_matrix = np.random.random(size=(size, 8))

    @dataclass
    class weightedClassifier:
        accuracy: float = 0.0
        weights: np.ndarray = np.array([])

    best = weightedClassifier()
    for weights in weight_matrix:
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
        if accuracy > best.accuracy:
            best.accuracy = accuracy
            best.weights = weights

    return best
