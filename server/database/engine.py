from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
import os
from pathlib import Path
from .models import Base, Word, User
from .secret import username, password, host, port, database, certs_path


url = f'cockroachdb://{username}:{password}@{host}:{port}/{database}?sslmode=verify-full&sslrootcert={certs_path}'

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
    anne = User(name='Anne C.')
    jey = User(name='Jey K.')
    justin = User(name='Justin X.')
    rachel = User(name='Rachel L.')
    team = (anne, jey, justin, rachel)

    run_transaction(
        Session,
        lambda s: s.add_all(team)
    )


# CONSTRUCT/DESTRUCT ###########################################################

def teardown():
    """
    Danger: this will destroy all existing tables.
    """
    Base.metadata.drop_all(engine)

def setup():
    Base.metadata.create_all(engine)
    create_words(limit=500)
    create_users()

def check():
    word_count = session.query(Word).count()
    print(f'Word count: {word_count}')
    assert(word_count > 0)
    okay = session.query(Word).filter(Word.word=='Okay')[0]
    print(okay)
    assert(okay.phonemes == 'OW2 K EY1')

    user_count = session.query(User).count()
    print(f'User count: {user_count}')
    assert(session.query(User).count() == 4)
    for user in session.query(User).all():
        print(user.id, user.name)


if __name__ == '__main__':
    # teardown()
    # setup()
    check()
