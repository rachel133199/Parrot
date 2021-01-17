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
        self.weights = [3, 1, 2, 3]   # [poor, good, new_random, new_similar]

    def get_next_word(self, user_id):
        potential_words = []    # [poor, good, new_random, new_similar]
        poor_words = performed_poorly_words(user_id, limit=1)
        good_words = performed_well_words(user_id, limit=1)
        new_random_words_list = new_random_words(user_id, limit=1)

        potential_words.append(self.first_or_random_word(poor_words))
        potential_words.append(self.first_or_random_word(good_words))
        potential_words.append(self.first_or_random_word(new_random_words_list))

        # new similar poor word or random
        if len(poor_words) > 0:
            potential_words.append(self.get_similar_word(user_id, poor_words[0].spelling))
        else:
            potential_words.append(random_words(count=1)[0].spelling)

        # crude method of enforcing a custom probability distribution
        potential_words_weighted = []
        for i, w in enumerate(potential_words):
            potential_words_weighted.extend([w]*self.weights[i])
        return random.choice(potential_words_weighted)

    def first_or_random_word(self, words):
        if len(words) > 0:
            return words[0]
        else:
            return random_words(count=1)[0]

    def get_similar_word(self, user_id, word):
        # returns random word if none found
        attempted_words = words_attempted(user_id)
        new_similar_words = []
        print(word)
        for _, w in self.model[word.upper()][:30]:
            if w not in attempted_words:
                new_similar_words.append(w)
        if len(new_similar_words) > 0:
            word = random.choice(new_similar_words)
            return get_word(word.lower().capitalize())
        else:
            return random_words(count=1)[0]

