# 🔍 ResumeLens - AI Resume Analyzer & Skill-Gap Roadmap

**Domain:** NLP · Information Retrieval · Career-Tech
**Level:** CSE (AI & ML) mini / major project
**Why it's useful:** Every student applying for placements/internships needs to know
*"How well does my resume match this job, and what should I learn next?"*

## Features
- Upload a resume (PDF/TXT) and paste any job description
- **Skill extraction** from a curated taxonomy (150+ skills, word-boundary safe: `c` ≠ `cloud`)
- **TF-IDF + cosine similarity** between resume and job description
- **Explainable ATS checks** (email, links, sections, impact numbers, length)
- **Weighted match score** (55% skills, 25% text similarity, 20% ATS)
- **Personalised learning roadmap** for each missing skill
- Downloadable report

## Architecture
```
Resume (PDF/TXT) ──► parser.py ──► clean text ─┐
                                               ├─► skills.py (taxonomy match)
Job description ───────────────────────────────┤
                                               └─► matcher.py (TF-IDF + ATS + score) ──► Streamlit UI
```

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
pytest
```
Try it with `samples/sample_resume.txt` and `samples/sample_jd.txt`.

## Structure
```
ResumeLens/
├── app.py
├── resumelens/ (parser.py, skills.py, matcher.py)
├── data/ (skills.json, resources.json)
├── samples/
├── tests/test_basic.py
└── requirements.txt
```

## Upgrade ideas (for higher marks)
1. **Semantic matching** with `sentence-transformers` (all-MiniLM-L6-v2) - catches "ML" vs "machine learning".
2. **Named Entity Recognition** with spaCy to extract skills not in the taxonomy.
3. **LLM feedback**: rewrite weak bullet points using an LLM API.
4. **Dataset evaluation**: use the Kaggle Resume Dataset and report precision/recall of skill extraction.
5. **Multi-job ranking**: upload one resume, rank 50 job descriptions.
6. **Deploy** on Streamlit Cloud / Hugging Face Spaces.

## Evaluation suggestions
- Hand-label 30 resumes; measure skill extraction precision/recall/F1.
- Compare TF-IDF vs sentence-embedding similarity against human match ratings.

## License
MIT
