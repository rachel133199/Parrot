import argparse
from collections import defaultdict
import itertools
from pathlib import Path
import enchant


d = enchant.Dict('en_CA')


class Pronunciation:
    def __init__(self, word, phonemes):
        self.word = word
        self.phonemes = phonemes

    def __str__(self):
        phonemes = ' '.join(self.phonemes)
        return f'{self.word}\t{" ".join(self.phonemes)}\n'

    def compressed_phonemes(self):
        return ''.join(
            Pronunciation.phone_to_char[phone[:2]]
            for phone in self.phonemes
        )


def words_by_frequency():
    words_seen = set()
    path = Path(__file__).parent / './frequencies_google.txt'
    with path.open() as f:
        for line in f:
            i = line.index('\t')
            word = line[:i].capitalize()
            if word in words_seen:
                continue

            words_seen.add(word)
            yield word.capitalize()


def phonemes_dict():
    phonemes_by_word = defaultdict(list)

    path = Path(__file__).parent / './phonemes.txt'
    with path.open() as f:
        for line in f:
            i = line.index(' ')
            word = line[:i].capitalize()

            if (j := word.find('(')) >= 0:
                word = word[:j]

            if not d.check(word):
                continue

            phonemes = line[i+1:-1].split()
            phonemes_by_word[word].append(phonemes)

    return phonemes_by_word


def pronunciations():
    phonemes_by_word = phonemes_dict()

    for word in words_by_frequency():
        # skip invalid single letters
        if len(word) <= 1 and word not in ('A', 'I'):
            continue

        # skip words with multiple pronunciations
        phonemes = phonemes_by_word[word]
        if len(phonemes) != 1:
            continue

        yield Pronunciation(word, phonemes[0])


def generate(n):
    path = Path(__file__).parent / f'./words/top_{n}.txt'
    with path.open('w') as f:
        for pronunciation in itertools.islice(pronunciations(), n):
            f.write(str(pronunciation))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=5000,
                        help='The number of words to output.')
    args = parser.parse_args()

    generate(args.top)
