import csv
from typing import Dict, List, Tuple


class Phonetic:
    """Add tags of HTML by pronunciations of English"""

    def __init__(self):
        with open('./src/english/dict/cmudict.tsv', mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=' ')
            # read_data[i][0]: word
            # read_data[i][1:]: phonetics
            read_data = [row for row in tsv_reader]
            self.dict_data: Dict[str, List[str]] = {read_data[i][0]: read_data[i][1:] for i in range(len(read_data))}

        with open('./src/english/dict/symbols.tsv', mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=' ')
            # symbols[i][0]: Arpabet
            # symbols[i][1:]: IPA symbol
            symbols = [row for row in tsv_reader]
            self.symbols: Dict[str, str] = {symbols[i][0]: str(symbols[i][1:]).lstrip("'[\'").rstrip("\']'") for i in range(len(symbols))}

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

        converted = self._fetch_phonetics(sentences)

        return ""

    def _fetch_phonetics(self, sentences: List[str]) -> List[Tuple[str, str]]:
        words: list = list()

        for word in sentences.strip(";:,.-_").split():
            phonetics: str = self._convert_ipa(self.dict_data[word.lower()])
            words.append((word, phonetics))

        return words

    def _convert_ipa(self, arpabets: List[str]) -> str:
        phonetics: str = ""
        for arpabet in arpabets:
            phonetics += self.symbols[arpabet]

        return phonetics

    @classmethod
    def _put_on(cls, word_list: List[Tuple[str, str]]) -> List[str]:
        pass
