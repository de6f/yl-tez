"""
    Give byte probability matrix and class vector
"""
import utils.config as config


def showHistogramForClasses(X, y):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(config.CLASSES.__len__(), 5))
    ax.hist(X, bins=15, stacked=True, rwidth=1.0, label=config.CLASSES)
    ax.legend()
