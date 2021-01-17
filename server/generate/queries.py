from sqlalchemy.sql.expression import func
from ..database.engine import session, Session
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


def update_performance(user_id, spelling, grade, r=0.5, b=50):
    spelling = spelling.capitalize()
    word = session.query(Performance).filter(spelling=spelling).first()
    if word is None:
        return # do nothing if we can't find the word

    performance = (
        session.query(Performance)
               .filter(user_id=user_id)
               .filter(word_id=word.id)
               .first()
    )
    if performance is None:
        run_transaction(
            Session,
            lambda s: s.add(Performance(
                user_id=user_id,
                word_id=word.id,
                grade=b*(1-r) + grade*r,
            ))
        )
    else:
        performance.grade = performance.grade * (1-r) + grade * r
        session.commit()
