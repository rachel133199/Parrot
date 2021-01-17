from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
import os
from pathlib import Path
from .models import Base, Word, User, Performance
from .secret import username, password, host, port, database, certs_path


url = f'cockroachdb://{username}:{password}@{database}.{host}:{port}/defaultdb?sslmode=verify-full&sslrootcert={certs_path}'

engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# FILL DATA ####################################################################

def create_words(chunk_size=500, limit=5000):
    path = Path(__file__).parent.parent.parent / './pronunciations/words/top_all.txt'
    new_words = Word.list_from_file(path)
    for i in range(0, min(len(new_words), limit), chunk_size):
        run_transaction(
            Session,
            lambda s: s.add_all(new_words[i:i+chunk_size])
        )

def create_users():
    anne = User(id=0, name='Anne C.')
    jey = User(id=1, name='Jey K.')
    justin = User(id=2, name='Justin X.')
    rachel = User(id=3, name='Rachel L.')
    team = (anne, jey, justin, rachel)

    run_transaction(
        Session,
        lambda s: s.add_all(team)
    )

def create_performances():
    jey_id = 1
    justin_id = 2
    zh_words = [
        'Asian',
        'Casual',
        'Conclusion',
        'Explosion',
        'Garage',
        'Genre',
        'Measure',
        'Occasionally',
        'Pleasure',
        'Treasure',
        'Version',
        'Vision',
    ]

    all_performances = []
    for word in session.query(Word).filter(Word.spelling.in_(zh_words)):
        all_performances.extend((
            Performance(user_id=jey_id, word_id=word.id, grade=80.0),
            Performance(user_id=justin_id, word_id=word.id, grade=20.0),
        ))
    run_transaction(
        Session,
        lambda s: s.add_all(all_performances)
    )


# CONSTRUCT/DESTRUCT ###########################################################

def teardown():
    """
    Danger: this will destroy all existing tables.
    """
    Base.metadata.drop_all(engine)

def setup():
    Base.metadata.create_all(engine)

    create_words()
    create_users()
    create_performances()

def check():
    word_count = session.query(Word).count()
    print(f'Word count: {word_count}')
    assert(word_count > 0)
    okay = session.query(Word).filter(Word.spelling=='Okay')[0]
    print(okay.id, okay.spelling, okay.phonemes)
    assert(okay.phonemes == 'OW2 K EY1')

    user_count = session.query(User).count()
    print(f'User count: {user_count}')
    assert(session.query(User).count() == 4)
    for user in session.query(User).all():
        print(user.id, user.name)

    performance_count = session.query(Performance).count()
    print(f'Performance count: {performance_count}')
    assert(performance_count == 12 * 2)


if __name__ == '__main__':
    # teardown()
    # setup()
    check()
