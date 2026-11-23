import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_long_instructor_names_are_truncated(monkeypatch):
    # The font is loaded relative to the repo root when the module is imported.
    monkeypatch.chdir(ROOT)
    spec = importlib.util.spec_from_file_location(
        "draw_schedule", ROOT / "cogs" / "helpers" / "draw_schedule.py"
    )
    draw_schedule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(draw_schedule)

    text = draw_schedule.get_draw_text(
        {
            "course": "CMPUT 174",
            "component": "LEC",
            "section": "A1",
            "class": "12345",
            "instructorName": "['Alexandria Bartholomew Wolfeschlegelsteinhausenbergerdorff']",
        },
        location="CAB 239",
    )

    assert text.splitlines()[-1].startswith("A. B. WOLFESCHLEGEL")
    assert text.endswith("...")
