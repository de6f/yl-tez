"""
    Give byte probability matrix and class vector
"""
import matplotlib.pyplot as plt

import utils.config as config


class VisualizeClasses:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.avg_byte_prob = {}

    # TODO: CLASS İSİMLERİ KULLANILIRSA DÜZELTİLMESİ LAZIM!
    def compute_class_avg(self):
        X = {i: [] for i in config.CLASSES}
        for x, label in zip(self.X, self.y):
            X[label].append(x)

        for key, value in X.items():
            self.avg_byte_prob[key] = [sum(x) for x in zip(*value)]

    def show_class_histogram(self):
        fig, ax = plt.subplots(figsize=(config.CLASSES.__len__(), 5))
        ax.hist(self.avg_byte_prob, bins=15, stacked=True, rwidth=1.0, label=config.CLASSES)
        ax.legend()
