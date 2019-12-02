import csv
from typing import Dict, List, Tuple


class IPA:
    """Add tags of HTML by pronunciations of English"""

    def __init__(self):
        with open('./src/english/dict/cmudict', mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=' ')
            # read_data[i][0]: word
            # read_data[i][1:]: phonetics
            read_data = [row for row in tsv_reader]
            self.dict_data: Dict[str, List[str]] = {read_data[i][0]: read_data[i][1:] for i in range(len(read_data))}

        with open('./src/english/dict/symbols', mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=' ')
            # symbols[i][0]: Arpabet
            # symbols[i][1:]: IPA symbol
            symbols = [row for row in tsv_reader]
            self.symbols: Dict[str, str] = {symbols[i][0]: symbols[i][1:] for i in range(len(symbols))}

        with open('./src/english/dict/vowels', mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=' ')
            self.vowels: Tuple[str] = [tuple(vowels) for vowels in tsv_reader][0]

    def export_html(self, text_post: str) -> str:
        """
        The text file change to HTML sentences.

        Args:
            text_post(str): Wish the text to add phonetics.

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

        phonetics = self._fetch_phonetics(sentences)
        converted: List[str] = self._put_on(phonetics)

        return "".join(converted)

    def _fetch_phonetics(self, sentences: List[str]) -> List[Tuple[str, str]]:
        """
        Convert text to list of originals and IPAs.

        Args:
            sentences: List[str]: To convert a text

        Returns:
            List[Tuple[str, str]: [(original word, IPA), ...]
        """
        words: list = list()

        # Remove non ascii characters
        is_after_vowel: bool = False
        phonetics: str = ""
        for sentence in sentences:
            sentence = reversed(sentence.split())
            for word in sentence:
                word = word.replace("<br>", "\n")
                target = word.strip(";:,.?-_<>|#\\\"\'\n")
                if target == "":
                    phonetics = ""
                elif target.lower() == "the" and is_after_vowel:
                    phonetics = "ðiː"
                    is_after_vowel = False
                else:
                    phonetics = self._convert_ipa(self.dict_data[target.lower()])
                    if phonetics.startswith(self.vowels):
                        is_after_vowel = True
                words.append((word, phonetics))
            words.append(("<br>\n", ""))
        words.reverse()
        return words

    def _convert_ipa(self, arpabets: List[str]) -> str:
        """
        Convert from Arpabet to IPA.

        Args:
            arpabets(List[str]): target word's Arpabet

        Returns:
            (str): IPA symbols
        """
        phonetics: str = ""
        for arpabet in arpabets:
            phonetics += self.symbols[arpabet][0]

        return phonetics

    @classmethod
    def _put_on(cls, word_list: List[Tuple[str, str]]) -> List[str]:
        sentences: List[str] = list()

        for word, phonetics in word_list:
            if phonetics is not "":
                sentences.append(f'<ruby class="under">{word}<rp>(</rp><rt>{phonetics}</rt><rp>)</rp></ruby> ')
            else:
                sentences.append(word)
        return sentences
