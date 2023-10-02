from kanshudo import KanshudoCrawler
from jmdict import JMDictParser
from kana import KanaService
from mongodb import MongoDBConnector
from dto import JMDictWordKanji, JMDictWordKana, KanaType, CompleteWord
from typing import List
from dotenv import load_dotenv
import os


def get_words() -> List[dict]:
    kshd = KanshudoCrawler()
    jmdict_parser = JMDictParser()
    kana_service = KanaService()

    complete_words = []
    words = kshd.get_words_on_all_pages()
    for word in words:
        jmdict_word = JMDictWordKanji(word.kanji) if word.kanji is not None else JMDictWordKana(word.kana)
        try:
            kana_type = KanaType.KATAKANA if kana_service.is_katakana(word.kana) else KanaType.HIRAGANA if kana_service.is_hiragana(word.kana) else None
            if kana_type is None:
                continue
            
            romaji = kana_service.to_romaji(word.kana)

            translations_eng = jmdict_parser.get_translations_by_word(jmdict_word)

            complete_words.append(
                CompleteWord(
                    **word.__dict__,
                    kana_type=kana_type, 
                    romaji=romaji,
                    translations_eng=translations_eng
                ).__dict__
            )
        except:
            continue
    return complete_words


def main():
    db = MongoDBConnector(
        db_name=os.environ['MONGODB_DB_NAME'], 
        username=os.environ['MONGODB_USERNAME'], 
        password=os.environ['MONGODB_PASS'], 
        cluster_uri=os.environ['MONGODB_CLUSTER_URI']
    ).db
    words = get_words()
    db.words.insert_many(words)


if __name__ == '__main__':
    load_dotenv()
    main()
