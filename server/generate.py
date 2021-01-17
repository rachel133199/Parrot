from sqlalchemy.sql.expression import func
from .database.engine import session
from .database.models import Word, User, Performance


def random_word():
    return session.query(Word).order_by(func.random())[0]


word = random_word()
print(word.rank, word.word, word.phonemes)
