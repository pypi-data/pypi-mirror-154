import re
from dataclasses import dataclass
from enum import Enum
from typing import Union


def slugify(text: str) -> str:
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"ï", "i", text)
    text = re.sub(r" ", "_", text)
    return text.lower()


class TheotexEnum(Enum):

    def __repr__(self):
        return self.value


class CorpusName(TheotexEnum):
    septante = "Septante"
    nouveau_testament = "Nouveau Testament"


class SeptuagintBookName(TheotexEnum):
    genese = "Genèse"
    exode = "Exode"
    levitique = "Lévitique"
    nombres = "Nombres"
    deuteronome = "Deutéronome"
    josue = "Josué"
    juges = "Juges"
    ruth = "Ruth"
    rois1 = "1 Rois"
    rois2 = "2 Rois"
    rois3 = "3 Rois"
    rois4 = "4 Rois"
    chroniques1 = "1 Chroniques"
    chroniques2 = "2 Chroniques"
    esdras1 = "1 Esdras"
    esdras2 = "2 Esdras"
    esther = "Esther"
    judith = "Judith"
    tobie = "Tobie"
    maccabees1 = "1 Maccabées"
    maccabees2 = "2 Maccabées"
    maccabees3 = "3 Maccabées"
    maccabees4 = "4 Maccabées"
    psaumes = "Psaumes"
    proverbes = "Proverbes"
    ecclesiastes = "Ecclésiastes"
    cantique = "Cantique"
    job = "Job"
    sagesse = "Sagesse"
    siracide = "Siracide"
    psaumes_de_salomon = "Psaumes de Salomon"
    osee = "Osée"
    amos = "Amos"
    michee = "Michée"
    joel = "Joël"
    abdias = "1bdias"
    jonas = "Jonas"
    nahum = "Nahum"
    habakuk = "Habakuk"
    sophonie = "Sophonie"
    aggee = "Aggée"
    zacharie = "Zacharie"
    malachie = "Malachie"
    esaie = "Esaïe"
    jeremie = "Jérémie"
    baruch = "Baruch"
    lamentations = "Lamentations"
    lettre_de_jeremie = "Lettre de Jérémie"
    ezechiel = "Ezéchiel"
    suzanne = "Suzanne"
    daniel = "Daniel"
    bel = "Bel"


class NewTestamentBookName(TheotexEnum):
    matthieu = "Matthieu"
    marc = "Marc"
    luc = "Luc"
    jean = "Jean"
    actes = "Actes"
    romains = "Romains"
    corinthiens1 = "1 Corinthiens"
    corinthiens2 = "2 Corinthiens"
    galates = "Galates"
    ephesiens = "Ephésiens"
    philippiens = "Philippiens"
    colossiens = "Colossiens"
    thessaloniciens1 = "1 Thessaloniciens"
    thessaloniciens2 = "2 Thessaloniciens"
    timothee1 = "1 Timothée"
    timothee2 = "2 Timothée"
    tite = "Tite"
    philemon = "Philémon"
    hebreux = "Hébreux"
    jacques = "Jacques"
    pierre1 = "1 Pierre"
    pierre2 = "2 Pierre"
    jean1 = "1 Jean"
    jean2 = "2 Jean"
    jean3 = "3 Jean"
    jude = "Jude"
    apocalypse = "Apocalypse"


CORPUS_NAMES = [slugify(member.value) for member in CorpusName.__members__.values()]
SEPTUAGINT_BOOK_NAMES = [member.value for member in SeptuagintBookName.__members__.values()]
NEW_TESTAMENT_BOOK_NAMES = [member.value for member in NewTestamentBookName.__members__.values()]
BIBLE_BOOK_NAMES = SEPTUAGINT_BOOK_NAMES + NEW_TESTAMENT_BOOK_NAMES


class Corpus(TheotexEnum):
    septante = "septuaginta"
    nouveau_testament = "ntgf"


class SeptuagintBook(TheotexEnum):
    genese = "genese"
    exode = "exode"
    levitique = "levitique"
    nombres = "nombres"
    deuteronome = "deuteronome"
    josue = "josue"
    juges = "juges"
    ruth = "ruth"
    rois1 = "1rois"
    rois2 = "2rois"
    rois3 = "3rois"
    rois4 = "4rois"
    chroniques1 = "1chroniques"
    chroniques2 = "2chroniques"
    esdras1 = "1esdras"
    esdras2 = "2esdras"
    esther = "esther"
    judith = "judith"
    tobie = "tobie"
    maccabees1 = "1maccabees"
    maccabees2 = "2maccabees"
    maccabees3 = "3maccabees"
    maccabees4 = "4maccabees"
    psaumes = "psaumes"
    proverbes = "proverbes"
    ecclesiastes = "ecclesiastes"
    cantique = "cantique"
    job = "job"
    sagesse = "sagesse"
    siracide = "siracide"
    psaumes_de_salomon = "salomon_psaumes"
    osee = "osee"
    amos = "amos"
    michee = "michee"
    joel = "joel"
    abdias = "abdias"
    jonas = "jonas"
    nahum = "nahum"
    habakuk = "habakuk"
    sophonie = "sophonie"
    aggee = "aggee"
    zacharie = "zacharie"
    malachie = "malachie"
    esaie = "esaie"
    jeremie = "jeremie"
    baruch = "baruch"
    lamentations = "lamentations"
    lettre_de_jeremie = "lettre_jeremie"
    ezechiel = "ezechiel"
    suzanne = "suzanne_theod"
    daniel = "daniel_theod"
    bel = "bel_theod"


class NewTestamentBook(TheotexEnum):
    matthieu = "matthieu"
    marc = "marc"
    luc = "luc"
    jean = "jean"
    actes = "actes"
    romains = "romains"
    corinthiens1 = "1corinthiens"
    corinthiens2 = "2corinthiens"
    galates = "galates"
    ephesiens = "ephesiens"
    philippiens = "philippiens"
    colossiens = "colossiens"
    thessaloniciens1 = "1thessaloniciens"
    thessaloniciens2 = "2thessaloniciens"
    timothee1 = "1timothee"
    timothee2 = "2timothee"
    tite = "tite"
    philemon = "philemon"
    hebreux = "hebreux"
    jacques = "jacques"
    pierre1 = "1pierre"
    pierre2 = "2pierre"
    jean1 = "1jean"
    jean2 = "2jean"
    jean3 = "3jean"
    jude = "jude"
    apocalypse = "apocalypse"


Book = Union[SeptuagintBook, NewTestamentBook]


@dataclass
class Verse:

    book: Book
    book_name: str
    book_greek_name: str
    chapter_num: int
    verse_num: str  # verse num is a string because some verses are referenced with a number and a letter like : "2c"
    french_version: str
    greek_version: str

    def __dict__(self):
        return {
            "book": self.book.value,
            "book_name": self.book_name,
            "book_greek_name": self.book_greek_name,
            "chapter_num": self.chapter_num,
            "verse_num": self.verse_num,
            "french_version": self.french_version,
            "greek_version": self.greek_version,
        }

    @property
    def get_french_str(self) -> str:
        return f"[{self.book_name}, {self.chapter_num}:{self.verse_num}] \"{self.french_version}\""

    @property
    def get_greek_str(self) -> str:
        return f"[{self.book_greek_name}, {self.chapter_num}:{self.verse_num}] \"{self.greek_version}\""

    def __str__(self):
        return f"{self.get_french_str}\n{self.get_greek_str}"


def get_book_from(key: str) -> Book | None:

    if key in SeptuagintBook.__members__.keys():
        return SeptuagintBook[key]

    if key in NewTestamentBook.__members__.keys():
        return NewTestamentBook[key]

    return None


def get_book_name_from(key: str) -> str | None:

    if key in SeptuagintBook.__members__.keys():
        return SeptuagintBookName[key].value

    if key in NewTestamentBook.__members__.keys():
        return NewTestamentBookName[key].value

    return None
