from sqlalchemy.sql.expression import func
from ..database.engine import session
from ..database.models import Word, User, Performance


def random_words(count):
    return session.query(Word).order_by(func.random())[:count]


def worst_words(user_id, limit):
    return (performance.word for performance in (
        session.query(Performance)
               .filter(user_id=user_id)
               .order_by(Performance.grade.asc())[:limit]
    ))
