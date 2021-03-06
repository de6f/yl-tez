
from io import StringIO

import matplotlib.pyplot as plt
import pydotplus
import seaborn
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.tree import export_graphviz

import utils.config as config


def show_metrics(results, y_test, truncate=False):
    if truncate:
        print("{} accuracy: {:.2f}, precision: {:.2f}, recall: {:.2f}, f-score: {:.2f}".format(
            results.__name__, accuracy_score(y_test, results.__results__),
            *precision_recall_fscore_support(y_test, results.__results__, average='macro')))
    else:
        print("{} accuracy: {}, precision: {}, recall: {}, f-score: {}".format(
            results.__name__, accuracy_score(y_test, results.__results__),
            *precision_recall_fscore_support(y_test, results.__results__, average='macro')))
    return accuracy_score(y_test, results.__results__)


# Plot confusion matrix
class modelCount:
    count = 1


def show_conf_matrix(results, y_test):
    if not config.SHOW_CONFUSION_MATRIX:
        return

    plt.figure()
    cm = confusion_matrix(y_test, results.__results__)
    hm = seaborn.heatmap(cm, annot=True, fmt=".1f", linewidths=1.0, square=1, cmap="OrRd")
    fig = hm.get_figure()
    fig.savefig("{}_{}".format(results.__name__, modelCount.count))
    modelCount.count += 1


# Save decision tree as a PNG
def dtree_viz(model, filename):
    dot_data = StringIO()
    export_graphviz(model, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(filename)
