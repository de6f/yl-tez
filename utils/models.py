
"""
    Model construction functions
"""
import numpy as np

from sklearn.model_selection import GridSearchCV

def DecisionTree(X, y):
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    params_dt = {'max_depth': np.arange(1,21), 'min_samples_leaf': [1, 5, 10, 20, 50, 100]}
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


# TODO: CVGridSearch'i kullan
def ArtificialNeuralNetwork(X, y):
    from sklearn.neural_network import MLPClassifier
    clf = MLPClassifier(hidden_layer_sizes=(50, 25, 25), solver='adam', learning_rate_init=0.01, max_iter=500)
    # params_ann = {'hidden_layer_sizes': }
    clf.fit(X, y)
    return clf


def XGBoost(X, y):
    import xgboost as xgb
    clf = xgb.XGBClassifier(random_state=1, learning_rate=0.01)
    clf.fit(X, y)
    return clf
