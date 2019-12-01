import re
from typing import Any, List, Tuple, Union

import jaconv
from janome.tokenizer import Tokenizer


class Phonetic:
    """Add tags of HTML by pronunciations of Kanji."""
    _has_instance = None

    def __new__(cls):
        if not cls._has_instance:
            cls._has_instance = super(Phonetic, cls).__new__(cls)
            cls.__re_compile()
            cls.token = Tokenizer()
        return cls._has_instance

    def export_html(self, text_post: str) -> str:
        """
        The text file change to HTML sentences.

        Args:
            text_post (str): Wish the text to add the ruby

        Returns:
            str: HTML format text
        """

        sentences: list = list()
        line: str = ""

        texts = "<br>\n".join(text_post.splitlines())

        for text in texts:
            for word in text:
                line += word
        sentences.append(line)

        fetch_char: List[Tuple[str]] = self._fetch_characters(sentences)
        phonetic_list: List[Tuple[str]] = self._remove_ascii_and_hiragana(
            fetch_char)
        converted: List[str] = self._put_on(phonetic_list)

        return "".join(converted)

    @classmethod
    def __re_compile(cls) -> None:
        """Regular expression patterns"""
        cls.re_hiragana = re.compile('[ぁ-ん]')
        cls.re_katakana = re.compile('[ァ-ン]')
        cls.re_zenkigou = re.compile('︰-＠')
        cls.re_kanji = re.compile('[一-龥]')
        cls.re_ascii = re.compile('[!-~]')

    def _fetch_characters(self, sentences: List[str]) -> List[Tuple[str]]:
        """
        Convert text to list of originals and Katakana.

        Args:
            sentences List[str]: To convert a text

        Returns:
            List[Tuple[str]]: [(original word, katakana), ...]
        """
        tokens: list = list()
        for sentence in sentences:
            tokens = self.token.tokenize(sentence)

        words: list = list()
        for token in tokens:
            words.append((token.surface, token.reading))
        return words

    def _remove_ascii_and_hiragana(self, words: List[Tuple[str]]
                                   ) -> List[Tuple[str]]:
        """
        Ascii and Hiragana aren't need pronunciation,
        So, this method are removing these.

        Args:
            words (List[Tuple[str]]): Phrases and pronunciations list
                i.e. [(original word, katakana), ...]

        Returns:
            List[Tuple[str]]: ascii and hiragana word is removing.
                    kanji -> hiragana
                    other  -> **None**
                i.e. [(word, reading), ...]]
        """
        new_words: list = list()
        for word, reading in words:
            if (re.search(self.re_kanji, word)
                    or re.search(self.re_zenkigou, word)):
                new_words.append((word, jaconv.kata2hira(reading)))
            else:
                new_words.append((word, ""))
        return new_words

    @classmethod
    def _put_on(cls, words_list: List[Tuple[str]]) -> List[str]:
        """
        Putting <ruby> tags on a text.

        Args:
            words_list (List[Tuple[str]]): Phrases and pronunciations list
                e.g. [("囲碁", "いご"), ...]
        Returns:
            List[str]: Text with <ruby> tags
                e.g. "<ruby>囲碁<rp>(</rp><rt>いご</rt><rp>)</rp></ruby>..."
        """

        sentences: List[str] = list()
        for word, reading in words_list:
            # Extract extra ruby char from word
            extra_char: list = re.findall(cls.re_hiragana, word)
            for char in extra_char:
                reading = reading.replace(char, "\u3000")
            if reading is not "":
                sentences.append(
                    f"<ruby>{word}<rp>(</rp><rt>{reading}</rt><rp>)</rp></ruby>"
                )
            else:
                sentences.append(word)
        return sentences
