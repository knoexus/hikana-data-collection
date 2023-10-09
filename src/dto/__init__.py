from typing import List

class KanshudoWord:
    def __init__(self, kanji: str | None, kana: str, pitch_chars: List[str] | None, occurence_level: int, jlpt_level: int) -> None:
        self.kanji = kanji
        self.kana = kana
        self.pitch_chars = pitch_chars
        self.occurence_level = occurence_level
        self.jlpt_level = jlpt_level
    
    def __str__(self) -> str:
        return f'Kanji: {self.kanji}; kana: {self.kana}, kana pitch chars: {self.pitch_chars if self.pitch_chars is None else ", ".join(self.pitch_chars)}, occurence level: {self.occurence_level}, jlpt level: {self.jlpt_level}'


class KanaType:
    HIRAGANA = 'hiragana'
    KATAKANA = 'katakana'


class CompleteWord(KanshudoWord):
    def __init__(self, kanji: str | None, kana: str, pitch_chars: List[str] | None, occurence_level: int, jlpt_level: int, kana_type: str, romaji: str, translations_eng: List[str]) -> None:
        super().__init__(kanji, kana, pitch_chars, occurence_level, jlpt_level)
        self.kana_type = kana_type
        self.romaji = romaji
        self.translations_eng = translations_eng

    def __str__(self) -> str:
        return f'{super().__str__()}, kana type: {self.kana_type}, romaji: {self.romaji}, english translations: {", ".join(self.translations_eng)}'
    

class JMDictWord:
    def __init__(self, text, tag) -> None:
        self.text = text
        self.tag = tag


class JMDictWordKanji(JMDictWord):
    def __init__(self, text) -> None:
        super().__init__(text, 'keb')


class JMDictWordKana(JMDictWord):
    def __init__(self, text) -> None:
        super().__init__(text, 'reb')