from pathlib import Path
from bs4 import BeautifulSoup
import pytest

from .patch import patch


@pytest.mark.parametrize("testname", ["test1", "test2", "test3", "test4", "test5"])
def test_happy_path(testname: str):
    original = Path("tests") / "assets" / f"{testname}.xml"
    target = Path("tests") / "assets" / f"{testname}_target.xml"

    actual = patch(original.read_text(), prettify=True)
    actual_soup = BeautifulSoup(actual, features="xml")
    wanted = target.read_text()
    wanted_soup = BeautifulSoup(wanted, features="xml")

    assert str(actual_soup) == str(wanted_soup)
