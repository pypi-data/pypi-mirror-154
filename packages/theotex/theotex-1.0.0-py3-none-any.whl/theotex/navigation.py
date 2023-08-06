from typing import List

__all__ = ["get_nb_chapters_for", "get_nb_verses_for", "get_all_verses_for", "get_verse_for", "get_verses_for"]

import bs4
import requests

from .util import Book, Verse
from . import urls
from . import util
from . import exceptions


def _get_markup_for(book: Book, chapter_num: int) -> bs4.BeautifulSoup:

    url: str
    request: requests.Response

    url = urls.construct_chapter_url(book, chapter_num)
    request = requests.get(url)
    request.encoding = "utf-8"
    return bs4.BeautifulSoup(request.text, "html.parser")


def _get_filtered_verse_table(html: bs4.BeautifulSoup) -> bs4.ResultSet:

    verse_rows: bs4.ResultSet

    verse_rows = html.body.table.tr.find_all("td")[8].find_all("tr")
    return [row for row in verse_rows if '<div class="num">' in str(row)]


def _get_verse_data_from_tag(tag: bs4.Tag) -> list:

    return [
        tag.find("div", class_="num").string,
        tag.find("div", class_="vf").text,
        tag.find("div", class_="vg").text.strip()
    ]


def _get_book_greek_name(html: bs4.BeautifulSoup) -> str:
    font = html.find("font", class_="tg")
    return font.text[:-2].strip().lower().capitalize()


def get_nb_chapters_for(book: Book) -> int:

    html: bs4.BeautifulSoup
    last_chapter_link: bs4.Tag

    html = _get_markup_for(book, 1)
    last_chapter_link = html.table.table.find_all("tr")[2].find_all("td")[2].find_all("a")[-1]

    return int(last_chapter_link.text)


def get_nb_verses_for(book: Book, chapter_num: int) -> int:

    html: bs4.BeautifulSoup

    html = _get_markup_for(book, chapter_num)

    return len(_get_filtered_verse_table(html))


def get_all_verses_for(book: Book, chapter_num: int) -> List[Verse]:

    html: bs4.BeautifulSoup
    verse_rows: bs4.ResultSet
    verses: List[Verse]

    verses = []
    html = _get_markup_for(book, chapter_num)
    verse_rows = _get_filtered_verse_table(html)

    book_name = util.get_book_name_from(book.name)
    book_greek_name = _get_book_greek_name(html)
    for row in verse_rows:

        row: bs4.Tag

        verses.append(Verse(book, book_name, book_greek_name, chapter_num, *_get_verse_data_from_tag(row)))

    return verses


def get_verse_for(book: Book, chapter_num: int, verse_ref: str) -> Verse:

    html: bs4.BeautifulSoup
    nb_chapters: int
    verse_refs: List[str]
    verse_rows: bs4.ResultSet

    nb_chapters = get_nb_chapters_for(book)

    if chapter_num > nb_chapters:
        raise exceptions.ChapterDoesNotExistError(f"Chapter n° {chapter_num} does not exist for {book.value}")

    html = _get_markup_for(book, chapter_num)
    verse_rows = _get_filtered_verse_table(html)
    verse_refs = [row.find("div", class_="num").string for row in verse_rows]

    if verse_ref not in verse_refs:
        raise exceptions.VerseDoesNotExistError(
            f"Verse n° {verse_ref} does not exist for chapter {chapter_num} in {book.value}"
        )

    verse_pos = verse_refs.index(verse_ref)
    verse = verse_rows[verse_pos]

    book_name = util.get_book_name_from(book.name)
    book_greek_name = _get_book_greek_name(html)

    return Verse(book, book_name, book_greek_name, chapter_num, *_get_verse_data_from_tag(verse))


def get_verses_for(book: Book, chapter_num: int, vrefs: List[str]) -> List[Verse]:

    verses: List[Verse]
    html: bs4.BeautifulSoup
    nb_chapters: int
    verse_refs: List[str]
    verse_rows: bs4.ResultSet
    verses: List[Verse]

    verses = []
    nb_chapters = get_nb_chapters_for(book)

    if len(vrefs) != 2:
        raise Exception("You need to give exactly 2 references in vrefs")

    if chapter_num > nb_chapters:
        raise exceptions.ChapterDoesNotExistError(f"Chapter n° {chapter_num} does not exist for {book.value}")

    html = _get_markup_for(book, chapter_num)
    verse_rows = _get_filtered_verse_table(html)
    verse_refs = [row.find("div", class_="num").string for row in verse_rows]

    for verse_ref in vrefs:
        if verse_ref not in verse_refs:
            raise exceptions.VerseDoesNotExistError(
                f"Verse n° {verse_ref} does not exist for chapter {chapter_num} in {book.value}"
            )

    beg_ref_index, end_ref_index = verse_refs.index(vrefs[0]), verse_refs.index(vrefs[1]) + 1
    if end_ref_index < beg_ref_index:
        raise Exception("Your references are in the wrong order")

    book_name = util.get_book_name_from(book.name)
    book_greek_name = _get_book_greek_name(html)
    for row in verse_rows[beg_ref_index:end_ref_index]:

        row: bs4.Tag

        verses.append(Verse(book, book_name, book_greek_name, chapter_num, *_get_verse_data_from_tag(row)))

    return verses
