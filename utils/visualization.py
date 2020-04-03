"""
    Give byte probability matrix and class vector
"""

import matplotlib.pyplot as plt
import numpy as np
import utils.config as config

class VisualizeClasses:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.avg_byte_prob = [None] * config.CLASS_COUNT

    # TODO: CLASS İSİMLERİ KULLANILIRSA DÜZELTİLMESİ LAZIM!
    def compute_class_avg(self):
        X = {i: [] for i in config.CLASSES}
        for x, label in zip(self.X, self.y):
            X[label].append(x)

        for key, value in X.items():
            self.avg_byte_prob[key-1] = [sum(x) for x in zip(*value)]

    def show_class_histogram(self):
        self.transpose_of_byte_prob = [list(x) for x in zip(*self.avg_byte_prob)]

        bins = 256
        plt.figure()
        plt.hist(self.transpose_of_byte_prob, bins, stacked=True, density=True)
        plt.title("Byte probability histogram of different malware classes")
        plt.show()