from wanakana import to_romaji, is_hiragana, is_katakana

class KanaService:
    def is_hiragana(self, text: str) -> bool:
        return is_hiragana(text)
    
    def is_katakana(self, text: str) -> bool:
        return is_katakana(text)
    
    def to_romaji(self, text: str) -> str:
        return to_romaji(text)