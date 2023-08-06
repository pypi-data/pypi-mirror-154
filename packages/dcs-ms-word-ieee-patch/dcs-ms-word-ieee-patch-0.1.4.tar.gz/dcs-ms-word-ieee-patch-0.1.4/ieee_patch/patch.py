from pathlib import Path
from typing import Any, List
import typer
from bs4 import BeautifulSoup
import xml.dom.minidom
from operator import itemgetter
from itertools import groupby
import copy
import zipfile
import sys
import logging
import shutil

app = typer.Typer()

logger = logging.Logger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)


def main():
    app()


@app.command(
    help=(
        "Patch IEEE citation format in Microsoft Word docx documents.\n\n"
        "The tool converts citations in the form '[1], [2], [3], [5]' to the "
        "IEEE compliant citation format [1-3,5]. "
        "An optional comma combined with spaces as separators between the "
        "citations are understood by the script."
    )
)
def run(
    fp: Path = typer.Argument(
        None,
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="Path to docx file that should be fixed.",
    ),
    overwrite: bool = typer.Option(
        False,
        help=(
            "Overwrites the file instead of creating a copy and working on the copy."
        ),
    ),
):
    try:
        if overwrite:
            new_fp = fp
        else:
            new_fp = _patch_filename(fp)
            shutil.copy(fp, new_fp)

        with zipfile.ZipFile(new_fp, "a") as archive:
            # The xml file that need to be patched is located in
            # `word/document.xml` and does contain all relevant content for the
            # whole document.
            path = Path("word", "document.xml").as_posix()
            with archive.open(path, "r") as fh:
                doc = fh.read().decode("utf-8")

            patched_doc = patch(doc)

            with archive.open(path, "w") as fh:
                fh.write(patched_doc.encode())
        sys.exit(0)

    except zipfile.BadZipFile as error:
        logger.error(error)
        sys.exit(1)


def _patch_filename(fp: Path):
    parts = list(fp.parts)
    fn = parts[-1].split(".")
    fn.insert(len(fn) - 1, "patched")
    parts[-1] = ".".join(fn)
    return Path(*parts)


def _create_simple_text_tag(soup: BeautifulSoup, char: str):
    tag = soup.new_tag("w:r", attrs={"w:rsidR": "007022E7"})
    tag2 = soup.new_tag("w:t")
    tag2.string = char
    tag.append(tag2)
    return tag


def rewrite_simple(bag: List[Any], strip: List[Any]):
    for i in range(1, len(bag) - 1):
        bag[i].extract()
    for el in strip:
        el.extract()


def get_cite_id(el) -> int:
    for tn in el.find_all("w:t"):
        if tn.text.strip() == "":
            continue

        # we found a match, see if we should keep it
        cite_digit: int = int(tn.text)
        return cite_digit

    return 0  # this case should never happen


def _strip_space_remove_brackets(el):
    text_nodes = el.find_all("w:t")
    for tn in text_nodes:
        # strip space-only nodes
        if tn.text.strip() == "":
            tn.parent.extract()  # remove any protected spaces
            continue

        # remove brackets
        tn.string = tn.text.strip()[1:-1]


def rewrite_complex(soup: BeautifulSoup, bag: List[Any], strip: List[Any]):
    # first remove all separating chars
    for el in strip:
        el.extract()

    for el in bag:
        _strip_space_remove_brackets(el)

    # 1. sort citations
    sbag = sorted(bag, key=lambda el: get_cite_id(el))
    sbag = [copy.copy(el) for el in sbag]  # deep copy for later rewrite
    ids = [get_cite_id(el) for el in sbag]

    # create hashmap
    sbag_map = {}
    for i, id_ in enumerate(ids):
        sbag_map[id_] = sbag[i]

    for i, el in enumerate(bag):  # change order of existing ones
        el.replace_with(sbag[i])

    # 2. remove duplicates
    seen = []
    for i, id_ in enumerate(ids[::-1]):
        if id_ not in seen:
            seen.append(id_)
            continue
        sbag.pop(i)
        ids.pop(i)
    del seen

    groups = []
    groups_iter = groupby(enumerate(ids), lambda x: x[0] - x[1])
    for _, g in groups_iter:
        groups.append(list(g))

    for i, g in enumerate(groups):
        group = map(itemgetter(1), g)
        group = list(map(int, group))
        if len(group) == 2:
            sbag_map[group[0]].insert_after(_create_simple_text_tag(soup, ","))
        if len(group) <= 2 and i != len(groups) - 1:
            sbag_map[group[-1]].insert_after(_create_simple_text_tag(soup, ","))
            continue
        for j, jx in enumerate(group):
            if j == 0:
                continue
            elif j == len(group) - 1:
                continue
            elif j == 1:
                # replace first middle element
                sbag_map[jx].replace_with(_create_simple_text_tag(soup, "-"))
            else:
                # remove all other middle elements
                sbag_map[jx].extract()

    sbag[0].insert_before(_create_simple_text_tag(soup, "["))
    sbag[-1].insert_after(_create_simple_text_tag(soup, "]"))


def patch(content: str, prettify: bool = False) -> str:
    soup = BeautifulSoup(content, features="xml")
    paragraphs = soup.find_all("w:p")

    bags = []
    strips = []
    for p in paragraphs:
        bag = []
        strip = []
        for child in p.children:
            # Remove any newline characters.
            if child.text == "\n":
                strip.append(child)
            # citations have the tag `w:sdt` and have a children `<w:citation/>`
            elif child.name == "sdt" and child.find("w:citation") is not None:
                bag.append(child)
            # If we have at least one element in the bag and the striped text
            # boils down to only a comma or no text at all, we are in between
            # two citations. Any stuff in between the citations should go to the
            # strip array.
            elif len(bag) > 0 and child.name == "r" and child.text.strip() in [",", ""]:
                strip.append(child)
            else:
                # register block (bag + strips)
                if len(bag) > 0:
                    bags.append(bag)
                    strips.append(strip)
                bag = []
                strip = []

        # register block if anything has been found which has not been registred yet
        if len(bag) > 0:
            if len(bag) > 0:
                bags.append(bag)
                strips.append(strip)
            bag = []
            strip = []

    for bag, strip in zip(bags, strips):
        rewrite_complex(soup, bag, strip)

    xml_content = str(soup).replace("\n", "")
    parsed = xml.dom.minidom.parseString(xml_content)
    if prettify:
        return parsed.toprettyxml()
    else:
        return parsed.toxml()


if __name__ == "__main__":
    app()
