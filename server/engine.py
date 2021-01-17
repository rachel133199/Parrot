from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from pathlib import Path


username = 'SECRET'
password = 'SECRET'
host = 'SECRET'
port = 26257
database = 'SECRET'
certs_path = Path(__file__).parent / './cc-ca.crt'

url = f'cockroachdb://{username}:{password}@{host}:{port}/{database}?sslmode=verify-full&sslrootcert={certs_path.absolute()}'

engine = create_engine(url, echo=True)

metadata = MetaData()


Base = declarative_base()


# WORD #########################################################################

class Word(Base):
    __tablename__ = 'words'

    rank = Column(Integer, primary_key=True, autoincrement=False)
    word = Column(String)
    phonemes = Column(String)
    phonemes_compressed = Column(String)


all_phonemes = [
    'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', # 01-10
    'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K',  # 11-20
    'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH',     # 21-30
    'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH',          # 31-39
]
compress_phoneme = {
    p : chr(i + ord('0') + 1)
    for i, p in enumerate(all_phonemes)
}
decompress_phoneme = {
    c : p for p, c in compress_phoneme.items()
}
def compress(p):
    return compress_phoneme[p[:2]]
def decompress(c):
    return decompress_phoneme[c]

def create_word(line, rank):
    i = line.index('\t')
    word = line[:i]
    phonemes = line[i+1:-1]
    phonemes_compressed = ''.join(compress(p) for p in phonemes.split())

    return Word(
        rank=rank,
        word=word,
        phonemes=phonemes,
        phonemes_compressed=phonemes_compressed,
    )


# USER #########################################################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

for phoneme in all_phonemes:
    setattr(User, phoneme.lower(), Column(String, default=0))


################################################################################

def reinit_tables():
    """
    Danger: this will destroy all existing tables.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_words(path, chunk_size=256):
    with path.open() as f:
        new_words = [
            create_word(line, rank=i+1)
            for i, line in enumerate(f)
        ]

    for pos in range(0, len(new_words), chunk_size):
        run_transaction(sessionmaker(bind=engine),
                        lambda s: s.add_all(new_words[pos:pos+chunk_size]))


if __name__ == '__main__':
    pass
    # path = Path(__file__).parent.parent / './pronunciations/words/top_1000.txt'
    # add_words(path)
