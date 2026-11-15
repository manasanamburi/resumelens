"""Skill extraction using a taxonomy with word-boundary matching."""
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load_taxonomy() -> dict:
    return json.loads((DATA / "skills.json").read_text(encoding="utf-8"))


def load_resources() -> dict:
    return json.loads((DATA / "resources.json").read_text(encoding="utf-8"))


def _pattern(skill: str) -> re.Pattern:
    # (?<![\w+#]) / (?![\w+#]) so 'c' does not match 'cloud' and 'c++' still works
    return re.compile(r"(?<![\w+#])" + re.escape(skill) + r"(?![\w+#])", re.IGNORECASE)


def extract_skills(text: str, taxonomy: dict | None = None) -> dict:
    """Return {category: [skills found]}."""
    taxonomy = taxonomy or load_taxonomy()
    found = {}
    for category, skills in taxonomy.items():
        hits = [s for s in skills if _pattern(s).search(text)]
        if hits:
            found[category] = hits
    return found


def flatten(found: dict) -> set:
    return {s for skills in found.values() for s in skills}
