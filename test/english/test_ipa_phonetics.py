import pytest

from src.english.ipa_phonetics import *


@pytest.mark.parametrize("sentence, expected", [
        ("This is a pen.", [('This', 'ðɪ́s'), ('is', 'ɪ́z'), ('a', 'ə'), ('pen.', 'pɜ́n')]),
        ("I just read the article on the newspaper.", [("I", 'áɪ'), ("just", 'ʤʌ́st'), ("read", 'rɜ́d'), ("the", 'ðiː'), ("article", 'ɑ́ːrtəkəl'), ("on", 'ɑ́ːn'), ("the", 'ðə'), ("newspaper.", 'núzpèɪpɜːr')])
])
def test_fetch_phonetics(sentence, expected):
    phonetic = IPA()

    actual = phonetic._fetch_phonetics(sentence)
    assert actual == expected


@pytest.mark.parametrize("word_list, expected", [
        ([('This', 'ðɪ́s')],
         ['<ruby class="under">This<rp>[</rp><rt>ðɪ́s</rt><rp>]</rp></ruby> ']),
        ([("the", 'ðiː'), ("article", 'ɑ́ːrtəkəl')],
         ['<ruby class="under">the<rp>[</rp><rt>ðiː</rt><rp>]</rp></ruby> ',
          '<ruby class="under">article<rp>[</rp><rt>ɑ́ːrtəkəl</rt><rp>]</rp></ruby> ']),
])
def test_put_on(word_list, expected):
    phonetic = IPA()

    actual = phonetic._put_on(word_list)
    assert actual == expected
