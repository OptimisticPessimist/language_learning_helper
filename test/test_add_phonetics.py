import pytest

import src.japanese.kana_phonetics as add_phonetic


class TestPhonetic:

    # yapf: disable
    @pytest.mark.parametrize("text, expected",
                                (
                                    (
                                        ["すももももももももの内"],
                                        [
                                            ("すもも", "スモモ"),
                                            ("も", "モ"),
                                            ("もも", "モモ"),
                                            ("も", "モ"),
                                            ("もも", "モモ"),
                                            ("の", "ノ"),
                                            ("内", "ウチ"),
                                        ],
                                    ),

                                    (
                                        ["まるで将棋だな"],
                                        [
                                            ("まるで", "マルデ"),
                                            ("将棋", "ショウギ"),
                                            ("だ", "ダ"),
                                            ("な", "ナ"),
                                        ],
                                    ),

                                    (
                                        ["FUJIカラーで写そう"],
                                        [
                                            ("FUJI", "*"),
                                            ("カラー", "カラー"),
                                            ("で", "デ"),
                                            ("写そ", "ウツソ"),
                                            ("う", "ウ")
                                        ],
                                    ),
                                )
                             )
    # yapf: enable
    def test_fetch_characters(self, text, expected):
        ruby = add_phonetic.Phonetic()
        actual = ruby._fetch_characters(text)
        assert actual == expected

    # yapf: disable
    @pytest.mark.parametrize("words, expected",
                                (
                                    (
                                        [
                                            ("すもも", "スモモ"),
                                            ("も", "モ"),
                                            ("もも", "モモ"),
                                            ("も", "モ"),
                                            ("もも", "モモ"),
                                            ("の", "ノ"),
                                            ("内", "ウチ"),
                                        ],
                                        [
                                            ("すもも", ""),
                                            ("も", ""),
                                            ("もも", ""),
                                            ("も", ""),
                                            ("もも", ""),
                                            ("の", ""),
                                            ("内", "うち"),
                                        ]
                                    ),
                                    (
                                        [
                                            ("まるで", "マルデ"),
                                            ("将棋", "ショウギ"),
                                            ("だ", "ダ"),
                                            ("な", "ナ"),
                                        ],
                                        [
                                            ("まるで", ""),
                                            ("将棋", "しょうぎ"),
                                            ("だ", ""),
                                            ("な", ""),
                                        ]
                                    ),
                                    (
                                        [
                                            ("FUJI", "*"),
                                            ("カラー", "カラー"),
                                            ("で", "デ"),
                                            ("写そ", "ウツソ"),
                                            ("う", "ウ")
                                        ],
                                        [
                                            ("FUJI", ""),
                                            ("カラー", ""),
                                            ("で", ""),
                                            ("写そ", "うつそ"),
                                            ("う", ""),
                                        ]
                                    )
                                )
                             )
    # yapf: enable
    def test_remove_ascii_and_hiragana(self, words, expected):
        ruby = add_phonetic.Phonetic()
        actual = ruby._remove_ascii_and_hiragana(words)
        assert actual == expected

    # yapf: disable
    @pytest.mark.parametrize("words_list, expected",
                             (
                                (
                                  [("囲碁", "いご"), ],
                                  ["<ruby>囲碁<rp>(</rp><rt>いご</rt><rp>)</rp></ruby>", ]
                                ),
                                (
                                  [("埋め込む", "うめこむ"), ],
                                  ["<ruby>埋め込む<rp>(</rp><rt>う　こ　</rt><rp>)</rp></ruby>", ]
                                ),
                             )
                            )
    # yapf: enable
    def test_put_on(self, words_list, expected):
        ruby = add_phonetic.Phonetic()
        actual = ruby._put_on(words_list)
        assert actual == expected
