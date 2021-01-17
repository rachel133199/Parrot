from .queries import random_words, new_random_words, performed_well_words, \
    performed_poorly_words, words_attempted, get_word
import joblib
from pathlib import Path
import random

_path = Path(__file__).parent / './similar_words.joblib'
_model = joblib.load(_path)


class WordRecommender:
    def __init__(self):
        self.model = _model
        self.categories = {'poor': 3, 'good': 1, 'new_random': 2, 'new_similar': 3}

    def get_next_word(self, user_id):
        potential_weighted_categories = []
        for c, weight in self.categories.items():
            potential_weighted_categories.extend([c]*weight)
        category = random.choice(potential_weighted_categories)

        if category == 'poor':
            return self.first_or_random_word(performed_poorly_words(user_id, limit=1))
        elif category == 'good':
            return self.first_or_random_word(performed_well_words(user_id, limit=1))
        elif category == 'new_random':
            return self.first_or_random_word(new_random_words(user_id, limit=1))
        else:
            poor_words = performed_poorly_words(user_id, limit=1)
            if len(poor_words) > 0:
                return self.get_similar_word(user_id, poor_words[0].spelling)
            else:
                return random_words(count=1)[0]

        return random_words(count=1)[0]

    def first_or_random_word(self, words):
        if len(words) > 0:
            return words[0]
        else:
            return random_words(count=1)[0]

    def get_similar_word(self, user_id, word):
        # returns random word if none found
        attempted_words = words_attempted(user_id)
        new_similar_words = []
        for _, w in self.model[word.upper()][:30]:
            if w not in attempted_words:
                new_similar_words.append(w)
        if len(new_similar_words) > 0:
            word = random.choice(new_similar_words)
            return get_word(word.lower().capitalize())
        else:
            return random_words(count=1)[0]

