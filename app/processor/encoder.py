import pickle
import numpy as np
from dir import get_full_path


def get_matrix(mail):
    file = get_full_path('data/psocols.txt')
    with open(file, 'rb') as f:
        lexicon = pickle.load(f)
    lex = np.zeros(len(lexicon))
    for word in mail:
        if word.lower() in lexicon:
            index_value = lexicon.index(word.lower())
            lex[index_value] += 1
    features = np.array(lex, dtype=np.float32)

    return features


