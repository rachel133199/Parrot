from sqlalchemy.sql.expression import func
from .database.engine import session
from .database.models import Word, User, Performance

THRESHOLD = 80


def new_random_word(user_id):
    words_attempted = set()
    for instance in session.query(Performance).filter(Performance.user_id == user_id):
        words_attempted.add(instance.word_id)   # TODO: change model to accommodate this
    return session.query(Word).filter(~Word.id.in_(words_attempted)).order_by(func.random())[0] # not in comparison


def performed_well_word(user_id):
    return session.query(Performance).filter(Performance.grade > THRESHOLD).join(Word).filter(Performance.user_id == user_id).order_by(func.random())[0]


def performed_poorly_word(user_id):
    return session.query(Performance).filter(Performance.grade <= THRESHOLD).join(Word).filter(Performance.user_id == user_id).order_by(func.random())[0]


word = new_random_word()
print(word.rank, word.word, word.phonemes)
