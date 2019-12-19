import pytest

from src.english.ipa_phonetics import *


@pytest.mark.parametrize("sentence, expected", [
        (["This is a pen."],
         [('This', 'ðɪ́s'), ('is', 'ɪ́z'), ('a', 'ə'), ('pen.', 'pɜ́n')]),
        (["I just read the article on the newspaper."],
         [("I", 'áɪ'), ("just", 'ʤʌ́st'), ("read", 'rɜ́d'),
          ("the", 'ðiː'), ("article", 'ɑ́ːrtəkəl'), ("on", 'ɑ́ːn'), ("the", 'ðə'), ("newspaper.", 'núzpèɪpɜːr')]),
        (['<Vocal>'], [("<Vocal>", "vóʊkəl")])
])
def test_fetch_phonetics(sentence, expected):
    phonetic = IPA()

    actual = phonetic._fetch_phonetics(sentence)
    assert actual == expected


@pytest.mark.parametrize("sentences, expected", [
        ("The quick onyx goblin jumps over the lazy dwarf.\nNow I Know My ABC's.",
         '<ruby class="under">The<rp>[</rp><rt>ðə</rt><rp>]</rp></ruby> <ruby class="under">quick<rp>[</rp><rt>kwɪ́k</rt><rp>]</rp></ruby> <ruby class="under">onyx<rp>[</rp><rt>ɑ́ːnɪks</rt><rp>]</rp></ruby> <ruby class="under">goblin<rp>[</rp><rt>ɡɑ́ːblɪn</rt><rp>]</rp></ruby> <ruby class="under">jumps<rp>[</rp><rt>ʤʌ́mps</rt><rp>]</rp></ruby> <ruby class="under">over<rp>[</rp><rt>óʊvɜːr</rt><rp>]</rp></ruby> <ruby class="under">the<rp>[</rp><rt>ðə</rt><rp>]</rp></ruby> <ruby class="under">lazy<rp>[</rp><rt>léɪziː</rt><rp>]</rp></ruby> <ruby class="under">dwarf.<rp>[</rp><rt>dwɔ́rf</rt><rp>]</rp></ruby><br>\n<ruby class="under">Now<rp>[</rp><rt>náʊ</rt><rp>]</rp></ruby> <ruby class="under">I<rp>[</rp><rt>áɪ</rt><rp>]</rp></ruby> <ruby class="under">Know<rp>[</rp><rt>nóʊ</rt><rp>]</rp></ruby> <ruby class="under">My<rp>[</rp><rt>máɪ</rt><rp>]</rp></ruby> <ruby class="under">ABC\'s.<rp>[</rp><rt>éɪbìːsìːz</rt><rp>]</rp></ruby> '
         ),
])
def test_export_html(sentences, expected):
    phonetic = IPA()

    actual = phonetic.export_html(sentences)
    assert actual == expected
