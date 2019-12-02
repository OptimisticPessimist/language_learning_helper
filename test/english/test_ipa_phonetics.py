import pytest

from src.english.ipa_phonetics import *

@pytest.mark.parametrize("sentence, expected", [
        ("This is a pen.", [('This', 'ðɪ́s'), ('is', 'ɪ́z'), ('a', 'ə'), ('pen', 'pɛn')]),
])
def test_fetch_phonetics(sentence, expected):
    phonetic = IPA()

    actual = phonetic._fetch_phonetics(sentence)
    assert actual == expected
