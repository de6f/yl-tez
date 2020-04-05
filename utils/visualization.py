
"""
    Give byte probability matrix and class vector
"""
import numpy as np
import matplotlib.pyplot as plt

import utils.config as config

class VisualizeClasses:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.avg_byte_prob = np.zeros((config.CLASS_COUNT, 256))

    # TODO: CLASS İSİMLERİ KULLANILIRSA DÜZELTİLMESİ LAZIM!
    def compute_class_avg(self):
        X = {i: [] for i in config.CLASSES}
        for x, label in zip(self.X, self.y):
            X[label].append(x)

        for key, value in X.items():
            self.avg_byte_prob[key-1] = np.array([sum(x) for x in zip(*value)]) / len(value)

    def show_class_histogram(self):
        plt.figure()
        plt.hist(x=self.avg_byte_prob, bins=25, range=[0,255], stacked=True)
        plt.title('Byte probability histogram of different malware classes')
        plt.show()