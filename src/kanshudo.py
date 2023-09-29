import requests
from bs4 import BeautifulSoup
from dto import KanshudoWord


class WordFinder:
    def get_string_between_substrings(self, string: str, substring1: str = '', substring2: str = '') -> str | None:
        try:
            return string[string.find(substring1)+len(substring1):string.rfind(substring2)]
        except BaseException:
            return None


class ExpandedRequests:
    def __init__(self) -> None:
        self.headers = { 'User-Agent': 'Mozilla/5.0' }
        self.soup_mode = 'html.parser'

    def get(self, *args, **kwargs) -> requests.Response:
        return requests.get(*args, **kwargs, headers=self.headers)
    
    def get_soup_content(self, *args, **kwargs) -> BeautifulSoup:
        html = self.get(*args, **kwargs).content
        return BeautifulSoup(html, self.soup_mode)


class KanshudoCrawler:
    def __init__(self) -> None:
        self.main_page_url = 'https://www.kanshudo.com/collections/vocab_usefulness2021'
        self.words_page_template_url = self.main_page_url + '/UFN2021-'
        self.words_page_template_offset = 100
        self.erequests = ExpandedRequests()
        self.word_finder = WordFinder()

    def get_level_word_counts(self) -> dict:
        soup = self.erequests.get_soup_content(self.main_page_url)
        title_elements = soup.select('.infopanel .title_h4')
        titles = [title_element.get_text() for title_element in title_elements]
        level_counts = [int(self.word_finder.get_string_between_substrings(title, '(', 'words)')) for title in titles]
        return dict((i + 1, value) for i, value in enumerate(level_counts))

    def get_words_on_all_pages(self) -> [KanshudoWord]:
        level_words_counts = self.get_level_word_counts()

        words = []
        for level, words_available in level_words_counts.items():
            current_page = 0
            while current_page * self.words_page_template_offset < words_available:
                words_on_one_page = self.get_words_on_one_page(level, current_page)
                words.extend(words_on_one_page)
                current_page += 1
                print(level, current_page)
        return words

    def get_words_on_one_page(self, level: int, page: int) -> [KanshudoWord]:
        url_postfix = f'{level}-{self.words_page_template_offset * page + 1}'
        words_page_url = self.words_page_template_url + url_postfix
        soup = self.erequests.get_soup_content(words_page_url)
        
        words = []
        jukugorows = soup.select('.jukugorow')
        for jukugorow in jukugorows:
            jukugo_element = jukugorow.select_one('.jukugo')
            kanji_element = jukugo_element.select_one('.f_kanji')
            furigana_element = jukugo_element.select_one('.furigana')
            if kanji_element is None and furigana_element is None:
                kanji = None
                kana = jukugo_element.select_one('a').get_text()
            else:
                kanji = kanji_element.get_text()
                kana = furigana_element.get_text()

            jlpt_element = jukugorow.select_one('.jlpt_container > span')
            jlpt_level = jlpt_element.get('class')[0][-1] if jlpt_element is not None else None

            model = KanshudoWord(kanji=kanji, kana=kana, occurence_level=level, jlpt_level=jlpt_level)
            words.append(model)
        return words