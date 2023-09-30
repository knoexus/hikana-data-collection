from kanshudo import KanshudoCrawler
from jmdict import JMDictParser

from dto import JMDictWordKanji, JMDictWordKana, CompleteWord

def main():
    kshd = KanshudoCrawler()
    jmdict_parser = JMDictParser()

    complete_words = []
    words = kshd.get_words_on_all_pages()
    for word in words:
        jmdict_word = JMDictWordKanji(word.kanji) if word.kanji is not None else JMDictWordKana(word.kana)
        try:
            translations = jmdict_parser.get_translations_by_word(jmdict_word)
            complete_words.append(CompleteWord(**word.__dict__, translations_eng=translations))
        except:
            continue
    return complete_words


if __name__ == '__main__':
    words = main()