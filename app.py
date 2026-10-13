import json
from pathlib import Path
 
import streamlit as st
 
DATA = Path(__file__).parent / "data"
candidates = json.loads((DATA / "candidates.json").read_text(encoding="utf-8"))
role = json.loads((DATA / "roles.json").read_text(encoding="utf-8"))[0]
 
st.set_page_config(page_title="Potential Lens", page_icon="🔍", layout="wide")
 
 
def keyword_hits(text):
    lowered = text.lower()
    return [k for k in role["keywords"] if k in lowered]
 
 
def passes_filter(text):
    return len(keyword_hits(text)) >= role["min_keyword_matches"]
 
 
def display_name(c, blind):
    return f"Candidate {c['id']}" if blind else c["name"]
 
 
# ---------- Sidebar ----------
st.sidebar.title("Potential Lens")
st.sidebar.caption("Find hidden potential, not just keywords.")
blind = st.sidebar.toggle("Blind mode (hide name, school, employer)", value=True)
st.sidebar.info(
    "Prototype: analyses are pre-generated for fictional candidates. "
    "A live AI call would replace the saved data."
)
 
# ---------- Header ----------
st.title("Potential Lens")
st.subheader(f"Target role: {role['title']}")
with st.expander("Job description and requirements"):
    st.write(role["description"])
    for r in role["requirements"]:
        st.write(f"- {r}")
 
tab1, tab2, tab3 = st.tabs(["Candidate analysis", "Keyword filter vs Potential Lens", "Responsible AI"])
 
# ---------- Tab 1: single candidate ----------
with tab1:
    options = {display_name(c, blind): c for c in candidates}
    choice = st.selectbox("Choose a candidate", list(options.keys()))
    c = options[choice]
    a = c["analysis"]
 
    left, right = st.columns([1, 1])
 
    with left:
        st.markdown("#### Resume")
        if not blind:
            st.caption(f"{c['school']} | {c['last_employer']}")
        st.text(c["resume"])
 
    with right:
        st.metric("Potential fit score", f"{a['fit_score']} / 100")
        st.progress(a["fit_score"] / 100)
        st.write(a["headline"])
 
        st.markdown("#### Transferable skills (with evidence)")
        for s in a["skills"]:
            st.markdown(f"**{s['skill']}**")
            st.caption(f"Evidence: \"{s['evidence']}\"")
 
        st.markdown("#### Growth signals")
        if a["growth_signals"]:
            for g in a["growth_signals"]:
                st.markdown(f"**{g['signal']}**")
                st.caption(f"Evidence: \"{g['evidence']}\"")
        else:
            st.write("No clear growth signals found in this resume.")
 
        st.markdown("#### Gaps to check")
        for gap in a["gaps"]:
            st.write(f"- {gap}")
 
    st.markdown("#### 90-day growth plan")
    p1, p2, p3 = st.columns(3)
    p1.info(f"**Days 1-30**\n\n{a['plan']['days_30']}")
    p2.info(f"**Days 31-60**\n\n{a['plan']['days_60']}")
    p3.info(f"**Days 61-90**\n\n{a['plan']['days_90']}")
 
    st.caption("Decision support only. A human makes the final hiring decision.")
 
# ---------- Tab 2: comparison ----------
with tab2:
    st.markdown(
        f"A typical filter keeps only resumes with at least **{role['min_keyword_matches']}** "
        f"of these keywords: {', '.join(role['keywords'])}."
    )
    rows = []
    for cand in candidates:
        hits = keyword_hits(cand["resume"])
        rows.append(
            {
                "Candidate": display_name(cand, blind),
                "Keywords matched": f"{len(hits)} / {len(role['keywords'])}",
                "Keyword filter": "Pass" if passes_filter(cand["resume"]) else "Rejected",
                "Potential Lens score": cand["analysis"]["fit_score"],
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.success(
        "Look at the Rejected rows with a high Potential Lens score. "
        "Those are the hidden gems a keyword filter would miss."
    )
 
# ---------- Tab 3: responsible AI ----------
with tab3:
    st.markdown(
        """
**What blind mode hides:** names, schools, and employers, so the analysis focuses on what the person did and learned.
 
**What it cannot fully remove:** other details can still hint at background, such as graduation years or club names.
 
**How we keep it accountable**
- Every inference is shown with a quote from the candidate's own resume.
- The tool supports HR and does not make the hiring decision.
- Sample candidates are fictional.
"""
    )
 