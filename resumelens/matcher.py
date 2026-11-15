"""Compare a resume with a job description and produce an actionable report."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import extract_skills, flatten, load_resources

SECTIONS = ["education", "experience", "projects", "skills", "certification", "achievements"]


def tfidf_similarity(resume: str, jd: str) -> float:
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    m = vec.fit_transform([resume, jd])
    return float(cosine_similarity(m[0], m[1])[0][0])


def ats_checks(resume: str) -> list:
    """Simple, explainable ATS-style checks. Returns [(passed, message)]."""
    low = resume.lower()
    words = len(resume.split())
    return [
        (bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume)), "Contains an email address"),
        (bool(re.search(r"linkedin\.com|github\.com", low)), "Links to LinkedIn / GitHub"),
        (all(s in low for s in ["education", "skills"]), "Has Education and Skills sections"),
        (any(s in low for s in ["projects", "experience", "internship"]), "Has Projects / Experience section"),
        (len(re.findall(r"\b\d+(\.\d+)?\s?%|\b\d{2,}\b", resume)) >= 3, "Uses numbers to show impact (%, counts)"),
        (250 <= words <= 900, f"Length is reasonable ({words} words; aim 250-900)"),
    ]


def analyze(resume: str, jd: str) -> dict:
    r_skills, j_skills = extract_skills(resume), extract_skills(jd)
    r_set, j_set = flatten(r_skills), flatten(j_skills)

    matched = sorted(r_set & j_set)
    missing = sorted(j_set - r_set)
    extra = sorted(r_set - j_set)

    skill_cov = len(matched) / len(j_set) if j_set else 0.0
    text_sim = tfidf_similarity(resume, jd)
    checks = ats_checks(resume)
    ats = sum(p for p, _ in checks) / len(checks)

    # Weighted score: skills matter most, then text similarity, then formatting
    score = round(100 * (0.55 * skill_cov + 0.25 * min(1, text_sim * 2.5) + 0.20 * ats), 1)

    resources = load_resources()
    roadmap = [(s, resources.get(s, f"Search '{s} tutorial' and build one mini project")) for s in missing]

    return {
        "score": score,
        "skill_coverage": round(skill_cov * 100, 1),
        "text_similarity": round(text_sim * 100, 1),
        "ats_score": round(ats * 100, 1),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "resume_skills": r_skills,
        "checks": checks,
        "roadmap": roadmap,
    }


def verdict(score: float) -> str:
    if score >= 75:
        return "Strong match - apply with confidence."
    if score >= 50:
        return "Decent match - close the missing skills and tailor your resume."
    return "Low match - build the missing skills with projects before applying."
