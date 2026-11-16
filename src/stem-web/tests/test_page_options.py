"""Tests for the model option selects on the page (REQ-004)."""

import json
import shutil
import subprocess
from html.parser import HTMLParser

import pytest
import stem_web
from stem_core.separation import ENSEMBLE_PRESETS, PASS_TWO_MODELS, SINGLE_STEMS

PAGE = (stem_web.static_dir() / "index.html").read_text()
SCRIPT = stem_web.static_dir() / "app.js"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


class SelectReader(HTMLParser):
    """Collects the option values and labels of each named select."""

    def __init__(self):
        super().__init__()
        self.selects: dict[str, list[tuple[str, str]]] = {}
        self._current = None
        self._value = None
        self._label = ""

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "select":
            self._current = values["name"]
            self.selects[self._current] = []
        elif tag == "option" and self._current:
            self._value = values.get("value", "")
            self._label = ""

    def handle_data(self, data):
        if self._value is not None:
            self._label += data

    def handle_endtag(self, tag):
        if tag == "option" and self._value is not None:
            self.selects[self._current].append((self._value, self._label.strip()))
            self._value = None
        elif tag == "select":
            self._current = None


def read_selects():
    reader = SelectReader()
    reader.feed(PAGE)
    return reader.selects


def test_req_004_the_page_holds_three_selects_with_a_default_option():
    selects = read_selects()
    assert set(selects) == {"model", "ensemble_preset", "single_stem"}
    for options in selects.values():
        assert options[0] == ("", "Default")


@pytest.mark.parametrize(
    "name, allowed",
    [
        ("model", PASS_TWO_MODELS),
        ("ensemble_preset", ENSEMBLE_PRESETS),
        ("single_stem", SINGLE_STEMS),
    ],
)
def test_req_004_each_select_lists_exactly_its_allowlist(name, allowed):
    values = [value for value, _ in read_selects()[name][1:]]
    assert values == list(allowed)


def run_option_fields(values):
    code = (
        "const { optionFields } = require(process.argv[1]);"
        "console.log(JSON.stringify(optionFields(JSON.parse(process.argv[2]))));"
    )
    result = subprocess.run(
        ["node", "-e", code, str(SCRIPT), json.dumps(values)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


@needs_node
def test_req_004_option_fields_keep_only_the_chosen_values():
    fields = run_option_fields({"model": "", "ensemble_preset": "karaoke", "single_stem": ""})
    assert fields == [["ensemble_preset", "karaoke"]]


@needs_node
def test_req_004_option_fields_return_nothing_for_all_defaults():
    assert run_option_fields({"model": "", "ensemble_preset": "", "single_stem": ""}) == []


def test_req_004_the_script_appends_the_option_fields_and_shows_the_detail_text():
    script = SCRIPT.read_text()
    assert "optionFields(" in script
    assert "data.append(" in script
    assert "body.detail" in script
