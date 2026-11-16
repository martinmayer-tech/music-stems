"""Tests for the stem links and the done-only rendering (REQ-004)."""

import json
import re
import shutil
import subprocess

import pytest
import stem_web

SCRIPT = stem_web.static_dir() / "app.js"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


def run_stem_links(job_id, stems):
    code = (
        "const { stemLinks } = require(process.argv[1]);"
        "console.log(JSON.stringify(stemLinks(process.argv[2], JSON.parse(process.argv[3]))));"
    )
    result = subprocess.run(
        ["node", "-e", code, str(SCRIPT), job_id, json.dumps(stems)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


@needs_node
def test_req_004_one_link_per_stem():
    links = run_stem_links("abc123", ["vocals.wav", "instrumental.wav"])
    assert links == [
        {"name": "vocals.wav", "url": "/jobs/abc123/stems/vocals.wav"},
        {"name": "instrumental.wav", "url": "/jobs/abc123/stems/instrumental.wav"},
    ]


@needs_node
def test_req_004_encodes_each_name():
    links = run_stem_links("abc123", ["lead vocal #1.wav"])
    assert links[0]["url"] == "/jobs/abc123/stems/lead%20vocal%20%231.wav"
    assert links[0]["name"] == "lead vocal #1.wav"


@needs_node
def test_req_004_a_job_with_no_stems_has_no_links():
    assert run_stem_links("abc123", []) == []


def test_req_004_player_and_link_exist_only_in_the_done_branch():
    script = SCRIPT.read_text()
    assert script.count('createElement("audio")') == 1
    assert script.count('setAttribute("download"') == 1
    # renderStem builds the player and the link. Only the done branch calls it.
    assert script.count("renderStem(") == 2
    done_branch = re.search(r'if \(job\.status === "done"\) \{(.*?)\n  \}', script, re.S)
    assert done_branch is not None
    assert "stemLinks(job.id, job.stems" in done_branch.group(1)
    assert "renderStem(link)" in done_branch.group(1)
