class KanshudoWord:
    def __init__(self, kanji: str | None, kana: str | None, occurence_level: int, jlpt_level: int) -> None:
        self.kanji = kanji
        self.kana = kana
        self.occurence_level = occurence_level
        self.jlpt_level = jlpt_level
    
    def __str__(self) -> str:
        return f'Kanji: {self.kanji}; kana: {self.kana}, occurence level: {self.occurence_level}, jlpt level: {self.jlpt_level}'