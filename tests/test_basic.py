from resumelens.skills import extract_skills, flatten
from resumelens.matcher import analyze


def test_word_boundaries():
    found = flatten(extract_skills("I love cloud computing and C++ and Python"))
    assert "c++" in found and "python" in found
    assert "c" not in found  # must not match inside 'cloud'


def test_analyze_gaps():
    resume = "Python SQL pandas. Education Skills Projects. me@x.com github.com/me"
    jd = "Need Python, SQL and Docker"
    res = analyze(resume, jd)
    assert "docker" in res["missing"]
    assert set(res["matched"]) == {"python", "sql"}
    assert 0 <= res["score"] <= 100
