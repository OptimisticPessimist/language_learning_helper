import pytest

from src.english.ipa_phonetics import *

@pytest.mark.parametrize("sentence, expected", [
        ("This is a pen.", [('This', 'ðɪ́s'), ('is', 'ɪ́z'), ('a', 'ə'), ('pen.', 'pɜ́n')]),
        ("I just read the article on the newspaper.", [("I", 'áɪ'), ("just", 'ʤʌ́st'), ("read", 'rɜ́d'), ("the", 'ðiː'), ("article", 'ɑ́ːrtəkəɫ'), ("on", 'ɑ́ːn'), ("the", 'ðə'), ("newspaper.", 'núzpèɪpɜːr')])
])
def test_fetch_phonetics(sentence, expected):
    phonetic = IPA()

    actual = phonetic._fetch_phonetics(sentence)
    assert actual == expected
