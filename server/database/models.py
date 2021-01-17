from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .phonemes import compress_phoneme


Base = declarative_base()


# WORD #########################################################################

class Word(Base):
    __tablename__ = 'words'

    rank = Column(Integer, primary_key=True, autoincrement=False)
    word = Column(String)
    phonemes = Column(String)
    phonemes_compressed = Column(String)

    performances = relationship('Performance', backref='word')

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
    def list_from_file(path):
        with path.open() as f:
            return list(
                Word.__from_line(line, rank=i+1)
                for i, line in enumerate(f)
            )


# USER #########################################################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    performances = relationship('Performance', backref='user')


# RESULT #######################################################################

class Performance(Base):
    __tablename__ = 'performance'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    word_rank = Column(Integer, ForeignKey('words.rank'), primary_key=True)
    grade = Column(Float)
    times_encountered = Column(Integer)
