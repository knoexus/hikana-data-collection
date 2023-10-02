from dto import KanshudoWord
from util.requests import ExpandedRequests
from util.words import WordFinder
from util.soup import Soup
from util.io import IO
from typing import List
from bs4 import BeautifulSoup
import os


class KanshudoCrawler:
    def __init__(self) -> None:
        self.kanshudo_local_dir = '../content/kanshudo-pages'
        self.main_page_url = 'https://www.kanshudo.com/collections/vocab_usefulness2021'
        self.words_page_template_url = self.main_page_url + '/UFN2021-'
        self.words_page_template_offset = 100
        self.word_finder = WordFinder()
        self.erequests = ExpandedRequests()

    def __get_words_on_one_page_url(self, level: int, page: int) -> str:
        url_postfix = f'{level}-{self.words_page_template_offset * page + 1}'
        return self.words_page_template_url + url_postfix
    
    def __get_page_soup(self, path: str, url: str) -> BeautifulSoup | None:
        if not os.path.isfile(path):
            html = self.erequests.get(url)
            IO.save_file(html, path)
            return Soup().get_soup_content(html)

        return Soup().load_soup_content(path)

    def __get_main_page_soup(self) -> BeautifulSoup | None:
        path = f'{self.kanshudo_local_dir}/main.html'
        return self.__get_page_soup(path, self.main_page_url)
    
    def __get_words_on_one_page_soup(self, level: int, page: int) -> BeautifulSoup | None:
        path = f'{self.kanshudo_local_dir}/{level}_{page}.html'
        url = self.__get_words_on_one_page_url(level, page)
        return self.__get_page_soup(path, url)

    def get_level_word_counts(self) -> dict:
        soup = self.__get_main_page_soup()
        title_elements = soup.select('.infopanel .title_h4')
        titles = [title_element.get_text() for title_element in title_elements]
        level_counts = [int(self.word_finder.get_string_between_substrings(title, '(', 'words)')) for title in titles]
        return dict((i + 1, value) for i, value in enumerate(level_counts))

    def get_words_on_all_pages(self) -> List[KanshudoWord]:
        level_words_counts = self.get_level_word_counts()

        words = []
        for level, words_available in level_words_counts.items():
            current_page = 0
            while current_page * self.words_page_template_offset < words_available:
                words_on_one_page = self.get_words_on_one_page(level, current_page)
                words.extend(words_on_one_page)
                current_page += 1
        return words

    def get_words_on_one_page(self, level: int, page: int) -> List[KanshudoWord]:
        soup = self.__get_words_on_one_page_soup(level, page)

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