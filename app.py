import streamlit as st
from resumelens import read_resume, analyze
from resumelens.matcher import verdict

st.set_page_config(page_title="ResumeLens", page_icon="🔍", layout="wide")
st.title("🔍 ResumeLens")
st.caption("Match your resume to a job, find skill gaps, and get a learning roadmap.")

left, right = st.columns(2)
with left:
    up = st.file_uploader("Upload resume (PDF/TXT)", type=["pdf", "txt"])
    pasted = st.text_area("...or paste resume text", height=180)
with right:
    jd = st.text_area("Paste the job description", height=290)

if st.button("Analyze", type="primary"):
    resume = read_resume(up) if up else read_resume(pasted)
    if not resume or not jd.strip():
        st.warning("Please provide both a resume and a job description.")
        st.stop()

    res = analyze(resume, jd)
    st.subheader(f"Overall match: {res['score']}/100")
    st.progress(min(int(res["score"]), 100))
    st.info(verdict(res["score"]))

    a, b, c = st.columns(3)
    a.metric("Skill coverage", f"{res['skill_coverage']}%")
    b.metric("Text similarity", f"{res['text_similarity']}%")
    c.metric("ATS checks", f"{res['ats_score']}%")

    s1, s2, s3 = st.columns(3)
    s1.success("**Matched skills**\n\n" + (", ".join(res["matched"]) or "None"))
    s2.error("**Missing skills**\n\n" + (", ".join(res["missing"]) or "None 🎉"))
    s3.info("**Extra skills you have**\n\n" + (", ".join(res["extra"]) or "None"))

    st.subheader("ATS checklist")
    for ok, msg in res["checks"]:
        st.write(("✅ " if ok else "❌ ") + msg)

    if res["roadmap"]:
        st.subheader("Learning roadmap for missing skills")
        for i, (skill, tip) in enumerate(res["roadmap"], 1):
            st.write(f"**{i}. {skill}** - {tip}")

    report = (f"ResumeLens report\nScore: {res['score']}/100\n"
              f"Matched: {', '.join(res['matched'])}\nMissing: {', '.join(res['missing'])}\n\n"
              + "\n".join(f"- {s}: {t}" for s, t in res["roadmap"]))
    st.download_button("Download report", report, "resumelens_report.txt")
