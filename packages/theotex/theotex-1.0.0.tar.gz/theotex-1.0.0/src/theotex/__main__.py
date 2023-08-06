__all__ = []

import sys
import string
from typing import List

import click

from . import __version__
from . import navigation
from . import util


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"""
    theotex, version {__version__}
    
    Datasource: https://theotex.org
    Developer: numbergazing
    Email: hello@numbergazing.com
    """)
    ctx.exit()


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    "-v", "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Output version information and exit"
)
def theotex():
    """Print Bible verses in French and Greek from https://theotex.org."""
    pass


@theotex.command()
def corpora() -> None:
    """Display a list of the available corpora."""
    click.echo("\n".join(util.CORPUS_NAMES))


@theotex.command()
@click.argument("corpus", type=click.STRING)
def books(corpus: str) -> None:
    """Display a list of the available books for a corpus."""

    corpus_slug: str
    book_list: List[str]

    corpus_slug = util.slugify(corpus)

    if corpus_slug not in util.CORPUS_NAMES:
        sys.exit(f"The corpus {corpus} does not exist.")

    match corpus_slug:
        case "septante":
            click.echo("\n".join(util.SEPTUAGINT_BOOK_NAMES))
        case "nouveau_testament":
            click.echo("\n".join(util.NEW_TESTAMENT_BOOK_NAMES))


@theotex.command()
@click.argument("book", type=click.STRING)
@click.argument("chapter", type=click.INT)
@click.argument("verses", type=click.STRING, metavar="[VERSE | VERSE:VERSE]")
@click.option("-f", "--french-only", is_flag=True, default=False, help="Display only the french verses.")
@click.option("-g", "--greek-only", is_flag=True, default=False, help="Display only the greek verses.")
def seek(book: str, chapter: int, verses: str, french_only: bool, greek_only: bool) -> None:
    """
        Display verses (theotex seek -h, for more info).

        Examples: Jean 3 16, Proverbes 3 5:6
    """

    message: str
    refs: List[str]
    book_slug: str
    verse_refs: List[str]
    filtered_refs: set

    message = str()
    book_slug = util.slugify(book)
    verse_refs = verses.split(":")
    filtered_refs = set(verse_refs) - {""}
    verse_refs = sorted(list(filtered_refs))

    if book_slug.startswith(tuple([digit for digit in string.digits])):
        book_slug = book_slug[2:] + book_slug[0]

    if french_only is True and greek_only is True:
        sys.exit("You can only use one of these options (--only-french, --only-greek) at a time.")

    if len(verse_refs) > 1:

        to_erase_index: int

        if french_only:
            to_erase_index = -1
        elif greek_only:
            to_erase_index = -1
        else:
            to_erase_index = -2

        for verse in navigation.get_verses_for(util.get_book_from(book_slug), chapter, verse_refs):
            if french_only:
                message += f"{verse.get_french_str}\n"
            elif greek_only:
                message += f"{verse.get_greek_str}\n"
            else:
                message += f"{str(verse)}\n\n"

        message = message[:to_erase_index]

    else:
        verse = navigation.get_verse_for(util.get_book_from(book_slug), chapter, verse_refs[0])
        if french_only:
            message = verse.get_french_str
        elif greek_only:
            message = verse.get_greek_str
        else:
            message = str(verse)

    click.echo(message)


if __name__ == "__main__":

    theotex()
    sys.exit(0)
