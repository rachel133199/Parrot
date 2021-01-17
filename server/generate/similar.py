import itertools
from itertools
import joblib
from pathlib import Path
import random


_path = Path(__file__).parent / './similar_words.joblib'
_model = joblib.load(_path)

def similar_words(word, limit): # an iterator for up to
    word = word.strip().upper()
    try:
        return (word.lower() for _, word in random.sample(_model[word], limit))
    except:
        return iter(()) # nothing

def similar_words_batch(words, limit):
    return set(itertools.chain.from_iterable(
        similar_words(word, limit)
        for word in words
    ))
