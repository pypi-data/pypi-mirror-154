import theotex
import theotex.util

HOME = "https://theotex.org"
SEPTUAGINT = f"{HOME}/{theotex.util.Corpus.septante.value}"
SEPTUAGINT_CHAPTER = SEPTUAGINT + "/{book}/{book}_{chapter_nb}.html"
NEW_TESTAMENT = f"{HOME}/{theotex.util.Corpus.nouveau_testament.value}"
NEW_TESTAMENT_CHAPTER = NEW_TESTAMENT + "/{book}/{book}_{chapter_nb}_gf.html"


def construct_chapter_url(book: theotex.util.Book, chapter: int) -> str:

    url: str

    if type(book) is theotex.util.SeptuagintBook:
        return SEPTUAGINT_CHAPTER.format(book=book.value, chapter_nb=chapter)
    else:
        return NEW_TESTAMENT_CHAPTER.format(book=book.value, chapter_nb=chapter)
