

import utils.config as config


"""
    Preprocessing
"""

from utils.preprocessing import preprocess

p = preprocess(config.BYTES_DIR, config.LABEL_FILE)

p()


"""
    BoW
"""

from utils.preprocessing import bag_of_words

bow = bag_of_words(config.BYTES_DIR, '2_0A32eTdBKayjCWhZqDOQ.seq')

hist = bow()

"""
    Load data set
"""