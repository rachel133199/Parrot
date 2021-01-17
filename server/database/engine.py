from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
import os
from pathlib import Path
from .models import Base, Word, User


username = os.environ['PARROT_DB_USERNAME']
password = os.environ['PARROT_DB_PASSWORD']
host = os.environ['PARROT_DB_HOST']
port = os.environ['PARROT_DB_PORT']
database = os.environ['PARROT_DB_DATABASE']
certs_path = Path(__file__).parent / './cc-ca.crt'

url = f'cockroachdb://{username}:{password}@{host}:{port}/{database}?sslmode=verify-full&sslrootcert={certs_path.absolute()}'

engine = create_engine(url, echo=True)


def teardown():
    """
    Danger: this will destroy all existing tables.
    """
    Base.metadata.drop_all(engine)


def add_words(path, chunk_size=500):
    new_words = Word.from_file(path)
    for i in range(0, len(new_words), chunk_size):
        run_transaction(
            sessionmaker(bind=engine),
            lambda s: s.add_all(new_words[i:i+chunk_size])
        )

def setup():
    Base.metadata.create_all(engine)

    path = Path(__file__).parent.parent.parent / './pronunciations/words/top_all.txt'
    add_words(path)


if __name__ == '__main__':
    print("Engine modules successfully setup.")
    # teardown()
    # setup()
