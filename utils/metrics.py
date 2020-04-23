from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support


def show_metrics(model, y_test):
    print('{} accuracy: {:.2f}, precision: {:.2f}, recall: {:.2f}, f-score: {:.2f}'.format(
        model.__name__, accuracy_score(y_test, model.__results__),
        *precision_recall_fscore_support(y_test, model.__results__, average='weighted')))


from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn

# Plot confusion matrix
def show_conf_matrix(model, y_test):
    plt.figure()
    cm = confusion_matrix(y_test, model.__results__)
    hm = seaborn.heatmap(cm, annot=True, fmt=".1f", linewidths=1.0, square=1)
    fig = hm.get_figure()
    fig.savefig(model.__name__)
