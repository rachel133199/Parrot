from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .phonemes import all_phonemes, compress_phoneme


Base = declarative_base()


# WORD #########################################################################

class Word(Base):
    __tablename__ = 'words'

    rank = Column(Integer, primary_key=True, autoincrement=False)
    word = Column(String)
    phonemes = Column(String)
    phonemes_compressed = Column(String)

    results = relationship('Result', back_populates='word')

    @staticmethod
    def __from_line(line, rank):
        i = line.index('\t')
        word = line[:i]
        phonemes = line[i+1:-1]
        phonemes_compressed = ''.join(
            compress_phoneme(p)
            for p in phonemes.split()
        )

        return Word(
            rank=rank,
            word=word,
            phonemes=phonemes,
            phonemes_compressed=phonemes_compressed,
        )

    @staticmethod
    def from_file(path):
        with path.open() as f:
            return list(
                Word.__from_line(line, rank=i+1)
                for i, line in enumerate(f)
            )


# USER #########################################################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    results = relationship('Result', back_populates='user')

for phoneme in all_phonemes:
    setattr(User, phoneme.lower(), Column(String, default=0))


# RESULT #######################################################################

class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey('users.id'))
    word = Column(Integer, ForeignKey('words.rank'))
