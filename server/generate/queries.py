from sqlalchemy.sql.expression import func
from ..database.engine import session
from ..database.models import Word, User, Performance

THRESHOLD = 80


def random_words(count):
    return session.query(Word).order_by(func.random())[:count]


def worst_words(user_id, limit):
    return (performance.word for performance in (
        session.query(Performance)
               .filter(user_id=user_id)
               .order_by(Performance.grade.asc())[:limit]
    ))


def new_random_words(user_id, limit):
    words_attempted = set()
    for instance in session.query(Performance).filter(Performance.user_id == user_id):
        words_attempted.add(instance.word_id)
    return session.query(Word).filter(~Word.id.in_(words_attempted)).order_by(func.random())[:limit] # not in comparison


def performed_well_words(user_id, limit):
    return [instance.word for instance in session.query(Performance).filter(Performance.grade >= THRESHOLD).filter(Performance.user_id == user_id).order_by(func.random())[:limit]]


def performed_poorly_words(user_id, limit):
    return [instance.word for instance in session.query(Performance).filter(Performance.grade < THRESHOLD).filter(Performance.user_id == user_id).order_by(func.random())[:limit]]


def get_word(word):
    return session.query(Word).filter(Word.spelling == word)[0]


def words_attempted(user_id):
    words_attempted = set()
    for instance in session.query(Performance).filter(Performance.user_id == user_id):
        words_attempted.add(instance.word_id)
    return words_attempted
