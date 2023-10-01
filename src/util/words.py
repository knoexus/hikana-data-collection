class WordFinder:
    def get_string_between_substrings(self, string: str, substring1: str = '', substring2: str = '') -> str | None:
        try:
            return string[string.find(substring1)+len(substring1):string.rfind(substring2)]
        except:
            return None