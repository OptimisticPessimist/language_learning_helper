import pytest

from src.english.ipa_phonetics import *

@pytest.mark.parametrize("sentence, expected", [
        ("This is a pen.", "dummy"),
])
def test_fetch_phonetics(sentence, expected):
    phonetic = Phonetic()

    actual = phonetic._fetch_phonetics(sentence)
    assert actual == expected
