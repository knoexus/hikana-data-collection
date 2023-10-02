import xml.etree.cElementTree as ET
import gzip
import io
import os
from util.requests import ExpandedRequests
from util.exceptions import JMDICT_ENTRY_NOT_FOUND_EXCEPTION
from util.io import IO
from dto import JMDictWord
from typing import List


class JMDictParser():
    def __init__(self) -> None:
        self.jmdict_local_path = '../content/JMdict_e'
        self.jmdict_download_url = 'http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz'
        self.erequests = ExpandedRequests()

        self.jmdict_root = self.__get_jmdict_root(not os.path.isfile(self.jmdict_local_path))

    def __download_jmdict_gzip(self) -> bytes:
        return self.erequests.get(self.jmdict_download_url)
    
    def __extract_jmdict_from_gzip(self, jmdict_gzip: bytes) -> bytes:
        with io.BytesIO(jmdict_gzip) as f_in:
            with gzip.open(f_in, 'rb') as f_out:
                return f_out.read()
            
    def __save_jmdict(self, jmdict: bytes) -> None:
        IO.save_file(jmdict, self.jmdict_local_path)
        
    def __get_jmdict_root(self, should_download: bool) -> ET.Element | None:
        if should_download:
            jmdict_gzip = self.__download_jmdict_gzip()
            jmdict = self.__extract_jmdict_from_gzip(jmdict_gzip)
            self.__save_jmdict(jmdict)
            return ET.fromstring(jmdict)

        return ET.parse(self.jmdict_local_path).getroot()

    def find_entry_by_word(self, word: JMDictWord) -> ET.Element | None:
        return self.jmdict_root.find(f'.//{word.tag}[.="{word.text}"].../...')

    def get_entry_translations(self, entry: ET.Element) -> List[str] | None:
        return [translation_element.text for translation_element in entry.find('sense').findall('gloss')]
    
    def get_translations_by_word(self, word: JMDictWord) -> List[str] | None:
        entry = self.find_entry_by_word(word)
        if entry is None:
            raise JMDICT_ENTRY_NOT_FOUND_EXCEPTION
        return self.get_entry_translations(entry)
