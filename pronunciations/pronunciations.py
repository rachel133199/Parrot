import argparse
from collections import defaultdict
import itertools
from pathlib import Path
import pickle


class Pronunciation:
    def __init__(self, word, phonemes):
        self.word = word
        self.phonemes = phonemes

    @staticmethod
    def from_str(self, line):
        # mainly for file I/O
        i = line.index('\t')
        word = line[:i]
        phonemes = line[i+1:-1].split()
        self.word = word
        self.phonemes = phonemes

    def __str__(self):
        return f'{self.word}\t{" ".join(self.phonemes)}\n'


def words_by_frequency():
    path = Path(__file__).parent / './frequencies.txt'
    with path.open() as f:
        count = 0
        for line in f:
            i = line.index('\t')
            word = line[:i]
            yield word


def phonemes_dict():
    phonemes_by_word = defaultdict(list)

    path = Path(__file__).parent / './phonemes.txt'
    with path.open() as f:
        for line in f:
            i = line.index(' ')
            word = line[:i].lower()

            if (j := word.find('(')) >= 0:
                word = word[:j]

            phonemes = line[i+1:-1].split()
            phonemes_by_word[word].append(phonemes)

    return phonemes_by_word


def pronunciations():
    phonemes_by_word = phonemes_dict()

    for word in words_by_frequency():
        # skip words that are too short
        if len(word) <= 1:
            continue

        # skip words with multiple pronunciations
        phonemes = phonemes_by_word[word]
        if len(phonemes) != 1:
            continue

        yield Pronunciation(word, phonemes[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10000,
                        help="The number of words to output.")
    args = parser.parse_args()

    for word in itertools.islice(pronunciations(), args.top):
        print(word, end='')
