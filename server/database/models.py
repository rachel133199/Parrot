from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .phonemes import compress_phoneme


Base = declarative_base()


# WORD #########################################################################

class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    spelling = Column(String, unique=True)
    phonemes = Column(String)
    phonemes_compressed = Column(String)

    performances = relationship('Performance', backref='word')

    @staticmethod
    def __from_line(line):
        i = line.index('\t')
        spelling = line[:i]
        phonemes = line[i+1:-1]
        phonemes_compressed = ''.join(
            compress_phoneme(p)
            for p in phonemes.split()
        )

        return Word(
            spelling=spelling,
            phonemes=phonemes,
            phonemes_compressed=phonemes_compressed,
        )

    @staticmethod
    def list_from_file(path):
        with path.open() as f:
            return list(Word.__from_line(line) for i, line in enumerate(f))


# USER #########################################################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    performances = relationship('Performance', backref='user')


# PERFORMANCE ##################################################################

class Performance(Base):
    __tablename__ = 'performance'

    word_id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    grade = Column(Float)
