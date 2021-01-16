import argparse
from collections import defaultdict
import itertools
from pathlib import Path
import enchant


d = enchant.Dict('en_CA')


class Pronunciation:
    phones = [
        'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', # 01-10
        'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K',  # 11-20
        'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH',     # 21-30
        'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH',          # 31-39
    ]
    phone_to_char = {
        phone : chr(i + ord('0') + 1)
        for i, phone in enumerate(phones)
    }
    char_to_phone = { char : phone for phone, char in phone_to_char.items() }

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
        phonemes = ' '.join(self.phonemes)
        return f'{self.word}\t{" ".join(self.phonemes)}\n'

    def compressed_phonemes(self):
        return ''.join(
            Pronunciation.phone_to_char[phone[:2]]
            for phone in self.phonemes
        )


def words_by_frequency():
    path = Path(__file__).parent / './frequencies.txt'
    with path.open() as f:
        count = 0
        for line in f:
            i = line.index('\t')
            word = line[:i]
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
            # print(pronunciation.compressed_phonemes())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=10000,
                        help='The number of words to output.')
    args = parser.parse_args()

    generate(args.top)
