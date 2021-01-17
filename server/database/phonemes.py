all_phonemes = [
    'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', # 01-10
    'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K',  # 11-20
    'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH',     # 21-30
    'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH',          # 31-39
]


def base_phoneme(p):
    """
    Extracts the base phoneme from a symbol which might have emphasis.
    """
    return p[:2]


_offset = ord('0') # just to make things readable
_compress_phoneme = {
    p : chr(i + _offset)
    for i, p in enumerate(all_phonemes)
}
def compress_phoneme(p):
    return _compress_phoneme[base_phoneme(p)]

def decompress_phoneme(c):
    return _decompress_phoneme[ord(c) - _offset]
