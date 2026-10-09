import os
import tempfile
import textwrap

import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from app.agents.resume_agent import analyze_resume
from app.agents.jd_agent import analyze_job_description
from app.services.matcher import calculate_match
from app.services.skill_gap import analyze_skill_gap
from app.services.career_recommender import recommend_careers
from app.services.ats_analyzer import calculate_ats_score
from app.services.ats_suggestions import generate_ats_suggestions


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JobSense AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HELPER FOR HTML
# ============================================================

def render_html(content):
    st.html(
        textwrap.dedent(content).strip()
    )
   

# ============================================================
# CUSTOM CSS
# ============================================================

render_html("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);


/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
[data-testid="stAppViewContainer"],
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 8% 0%,
            rgba(99, 102, 241, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 8%,
            rgba(168, 85, 247, 0.11),
            transparent 25%
        ),
        #080b14;

    color: #f8fafc;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b0f1a 0%,
            #090c15 100%
        );

    border-right: 1px solid rgba(255,255,255,0.07);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.8rem;
}

.sidebar-brand {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.6px;
}

.sidebar-brand span {
    color: #818cf8;
}

.sidebar-subtitle {
    color: #7f8aa3;
    font-size: 12px;
    margin-top: 4px;
    margin-bottom: 28px;
}

.sidebar-info {
    padding: 16px;
    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            rgba(99,102,241,0.10),
            rgba(139,92,246,0.04)
        );

    border: 1px solid rgba(129,140,248,0.15);
}

.sidebar-info-title {
    color: #c7d2fe;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 9px;
}

.sidebar-info-text {
    color: #8e99ad;
    font-size: 12px;
    line-height: 1.8;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    width: 100%;
    box-sizing: border-box;

    padding: 38px 42px;
    margin-bottom: 30px;

    border-radius: 26px;

    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.19),
            rgba(168,85,247,0.09),
            rgba(15,23,42,0.78)
        );

    border: 1px solid rgba(139,92,246,0.24);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.24);

    overflow: hidden;
}

.hero-badge {
    display: inline-flex;
    align-items: center;

    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(99,102,241,0.13);
    border: 1px solid rgba(129,140,248,0.24);

    color: #a5b4fc;

    font-size: 12px;
    font-weight: 700;

    letter-spacing: 0.5px;
}

.hero-title {
    margin: 17px 0 0 0;

    color: #ffffff;

    font-size: clamp(32px, 4vw, 52px);

    line-height: 1.08;

    font-weight: 800;

    letter-spacing: -1.5px;
}

.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #818cf8,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 850px;

    margin-top: 16px;

    color: #a7b0c2;

    font-size: 15px;

    line-height: 1.75;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    color: #f8fafc;

    font-size: 23px;
    font-weight: 750;

    margin-top: 25px;
    margin-bottom: 15px;

    letter-spacing: -0.4px;
}


/* =========================================================
   JD INPUT
   ========================================================= */

div[data-testid="stTextArea"] textarea {
    min-height: 220px !important;

    background: #0d1322 !important;

    color: #f8fafc !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 16px !important;

    font-size: 14px !important;

    line-height: 1.6 !important;

    padding: 16px !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(129,140,248,0.60) !important;

    box-shadow:
        0 0 0 1px rgba(129,140,248,0.25) !important;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.55);

    border-radius: 16px;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(15,23,42,0.65) !important;

    border:
        1px dashed
        rgba(129,140,248,0.25) !important;

    border-radius: 15px !important;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;

    min-height: 50px;

    border-radius: 13px;

    border:
        1px solid
        rgba(129,140,248,0.35);

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

    color: #ffffff;

    font-size: 15px;
    font-weight: 700;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 30px
        rgba(99,102,241,0.28);
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-card {
    min-height: 132px;

    padding: 21px;

    box-sizing: border-box;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(20,27,48,0.96),
            rgba(12,17,30,0.96)
        );

    border:
        1px solid
        rgba(255,255,255,0.075);

    box-shadow:
        0 12px 35px
        rgba(0,0,0,0.17);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);

    border-color:
        rgba(129,140,248,0.38);
}

.metric-label {
    color: #8e99ad;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.8px;
}

.metric-value {
    color: #ffffff;

    font-size: 31px;
    font-weight: 800;

    margin-top: 9px;

    word-break: break-word;
}


/* =========================================================
   PANELS
   ========================================================= */

.panel {
    height: 100%;
    box-sizing: border-box;

    padding: 22px;

    border-radius: 18px;

    background:
        rgba(15,23,42,0.70);

    border:
        1px solid
        rgba(255,255,255,0.07);
}

.panel-title {
    color: #ffffff;

    font-size: 17px;
    font-weight: 700;

    margin-bottom: 14px;
}


/* =========================================================
   SKILL BADGES
   ========================================================= */

.skill-card,
.missing-card {
    display: inline-flex;

    align-items: center;

    padding: 8px 12px;

    margin:
        4px
        4px
        4px
        0;

    border-radius: 10px;

    font-size: 12px;
    font-weight: 600;

    white-space: normal;

    max-width: 100%;
}

.skill-card {
    color: #c7d2fe;

    background:
        rgba(99,102,241,0.10);

    border:
        1px solid
        rgba(129,140,248,0.22);
}

.missing-card {
    color: #fca5a5;

    background:
        rgba(239,68,68,0.08);

    border:
        1px solid
        rgba(248,113,113,0.22);
}


/* =========================================================
   CAREER CARDS
   ========================================================= */

.career-card {
    padding: 20px;

    margin-bottom: 10px;

    border-radius: 16px;

    background:
        rgba(15,23,42,0.75);

    border:
        1px solid
        rgba(255,255,255,0.07);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.career-card:hover {
    transform: translateX(4px);

    border-color:
        rgba(129,140,248,0.38);
}

.career-rank {
    color: #818cf8;

    font-size: 11px;
    font-weight: 700;

    letter-spacing: 0.6px;
}

.career-name {
    color: #ffffff;

    font-size: 18px;
    font-weight: 700;

    margin:
        5px
        0
        8px
        0;
}

.career-score {
    color: #a5b4fc;

    font-size: 13px;
    font-weight: 700;
}


/* =========================================================
   PROGRESS
   ========================================================= */

.stProgress {
    margin-bottom: 12px;
}

.stProgress > div > div > div > div {
    border-radius: 20px;
}


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {
    background: rgba(15,23,42,0.55);

    border:
        1px solid
        rgba(255,255,255,0.07);

    border-radius: 15px;
}


/* =========================================================
   EMPTY STATE
   ========================================================= */

.empty-state {
    width: 100%;
    box-sizing: border-box;

    margin-top: 32px;

    padding: 35px 25px;

    text-align: center;

    border-radius: 20px;

    border:
        1px dashed
        rgba(129,140,248,0.22);

    background:
        rgba(15,23,42,0.35);
}

.empty-icon {
    font-size: 40px;
}

.empty-title {
    color: #ffffff;

    font-size: 20px;
    font-weight: 700;

    margin-top: 10px;
}

.empty-text {
    color: #7f8aa3;

    font-size: 13px;

    line-height: 1.6;

    margin-top: 8px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #667085;

    font-size: 11px;

    line-height: 1.7;

    margin-top: 45px;

    padding-top: 20px;

    border-top:
        1px solid
        rgba(255,255,255,0.06);
}


/* =========================================================
   TABLET
   ========================================================= */

@media (max-width: 1100px) {

    .block-container {
        padding-left: 1.8rem;
        padding-right: 1.8rem;
    }

    .hero {
        padding: 32px;
    }

    .metric-value {
        font-size: 27px;
    }
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2.5rem;

        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 25px 20px;

        border-radius: 20px;

        margin-bottom: 22px;
    }

    .hero-badge {
        font-size: 10px;

        padding: 7px 10px;

        letter-spacing: 0.3px;
    }

    .hero-title {
        font-size: 32px;

        letter-spacing: -0.8px;
    }

    .hero-subtitle {
        font-size: 13px;

        line-height: 1.65;
    }

    .section-title {
        font-size: 20px;

        margin-top: 20px;
    }

    .metric-card {
        min-height: 110px;

        padding: 17px;
    }

    .metric-value {
        font-size: 25px;
    }

    .metric-label {
        font-size: 10px;
    }

    .panel {
        padding: 18px;
    }

    .career-card {
        padding: 17px;
    }

    .career-name {
        font-size: 16px;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 190px !important;

        font-size: 13px !important;
    }

    .empty-state {
        padding:
            28px
            18px;
    }
}


/* =========================================================
   SMALL MOBILE
   ========================================================= */

@media (max-width: 480px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .hero-title {
        font-size: 28px;
    }

    .hero-subtitle {
        font-size: 12px;
    }

    .metric-card {
        min-height: 100px;
    }

    .metric-value {
        font-size: 23px;
    }

    .skill-card,
    .missing-card {
        font-size: 11px;

        padding: 7px 9px;
    }

    .empty-title {
        font-size: 18px;
    }
}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-brand">
        💼 JobSense <span>AI</span>
    </div>

    <div class="sidebar-subtitle">
        Resume Intelligence Platform
    </div>
    """)

    st.markdown("### 📄 Your Resume")

    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload your latest resume in PDF format.",
    )

    if resume_file is not None:

        st.success(
            f"✓ {resume_file.name}"
        )

    st.markdown("---")

    render_html("""
    <div class="sidebar-info">

        <div class="sidebar-info-title">
            ✨ What JobSense AI does
        </div>

        <div class="sidebar-info-text">
            • Resume skill extraction<br>
            • Job matching<br>
            • Skill gap analysis<br>
            • Career recommendations
        </div>

    </div>
    """)

    st.markdown("")

    st.caption(
        "Built with Python + Streamlit"
    )


# ============================================================
# HERO
# ============================================================

render_html("""
<div class="hero">

    <div class="hero-badge">
        ✨ SMART CAREER INTELLIGENCE
    </div>

    <h1 class="hero-title">
        Know your
        <span class="hero-gradient"> job fit.</span>
        <br>
        Build your career smarter.
    </h1>

    <div class="hero-subtitle">
        Analyze your resume against any job description,
        discover missing skills, and identify career roles
        that match your current profile.
    </div>

</div>
""")


# ============================================================
# JOB DESCRIPTION
# ============================================================

render_html("""
<div class="section-title">
    💼 Analyze a Job
</div>
""")

jd_text = st.text_area(
    "Job Description",
    height=220,
    placeholder=(
        "Paste the complete job description here...\n\n"
        "Example:\n"
        "We are looking for a Data Scientist with Python, SQL, "
        "Machine Learning, Pandas and Scikit-learn..."
    ),
    label_visibility="collapsed",
)


analyze_button = st.button(
    "🚀 Analyze My Job Fit",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if resume_file is None:

        st.warning(
            "📄 Please upload your resume PDF from the sidebar."
        )

        st.stop()

    if not jd_text.strip():

        st.warning(
            "💼 Please paste a Job Description above."
        )

        st.stop()


    with st.spinner(
        "🔍 Analyzing your resume and job description..."
    ):

        temp_path = None

        try:

            # ------------------------------------------------
            # Temporary resume file
            # ------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    resume_file.getbuffer()
                )

                temp_path = temp_file.name


            # ------------------------------------------------
            # Resume Analysis
            # ------------------------------------------------

            resume_text = extract_text_from_pdf(
                temp_path
            )

            resume_data = analyze_resume(
                resume_text
            )


            # ------------------------------------------------
            # Job Description Analysis
            # ------------------------------------------------

            jd_data = analyze_job_description(
                jd_text
            )


            # ------------------------------------------------
            # Match
            # ------------------------------------------------

            match_result = calculate_match(
                resume_data["skills"],
                jd_data["required_skills"]
            )

            ats_result = calculate_ats_score(
                resume_text,
                resume_data["skills"],
                jd_data["required_skills"]
            )

            ats_suggestions = generate_ats_suggestions(
    resume_text=resume_text,
    resume_skills=resume_data["skills"],
    jd_skills=jd_data["required_skills"],
    ats_result=ats_result
)
            # ------------------------------------------------
            # Skill Gap
            # ------------------------------------------------

            gap_skills = match_result.get(
            "semantic_missing_skills",
            match_result["missing_skills"]
            )

            skill_gap = analyze_skill_gap(
            gap_skills
            )

            # ------------------------------------------------
            # Career Recommendations
            # ------------------------------------------------

            career_recommendations = recommend_careers(
                resume_data["skills"],
                jd_data["required_skills"]
            )


            # ------------------------------------------------
            # Store results
            # ------------------------------------------------

            st.session_state["analysis_result"] = {
            "resume_data": resume_data,
            "jd_data": jd_data,
            "match_result": match_result,
            "ats_result": ats_result,
            "skill_gap": skill_gap,
            "career_recommendations": career_recommendations,
            "ats_suggestions": ats_suggestions,
}


        except Exception as error:

            st.error(
                "Something went wrong while analyzing the files."
            )

            st.exception(error)

        finally:

            if temp_path and os.path.exists(temp_path):

                try:
                    os.remove(temp_path)

                except OSError:
                    pass

# ============================================================
# DISPLAY RESULTS
# ============================================================

if "analysis_result" in st.session_state:

        result = st.session_state["analysis_result"]
        resume_data = result["resume_data"]
        match_result = result["match_result"]
        ats_result = result.get("ats_result", {})
        ats_suggestions = result.get("ats_suggestions", [])
        skill_gap = result["skill_gap"]
        career_recommendations = result["career_recommendations"]

    # ========================================================
    # SCORE VALUES
    # ========================================================

        final_score = match_result.get("match_score", 0)
        keyword_score = match_result.get("keyword_score", 0)
        semantic_score = match_result.get("semantic_score", 0)

        ats_score = ats_result.get("ats_score", 0)

        exact_matches = match_result.get(
        "matched_skills",
        []
    )

        semantic_matches = match_result.get(
            "semantic_matched_skills",
            []
        )

        weak_matches = match_result.get(
            "weak_matches",
        []
    )

        missing_skills = match_result.get(
            "semantic_missing_skills",
            match_result.get("missing_skills", [])
        )

    # ========================================================
    # JOB FIT HEADER
    # ========================================================

        render_html("""
        <div class="section-title">
            🎯 Your Job Fit
        </div>
        """)

        if final_score >= 80:
            score_status = "Excellent Match"
        elif final_score >= 60:
            score_status = "Good Match"
        elif final_score >= 40:
            score_status = "Moderate Match"
        else:
            score_status = "Needs Improvement"

        # ========================================================
        # MAIN SCORE CARDS
        # ========================================================

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium"
        )

        with col1:

            render_html(f"""
            <div class="metric-card">

                <div class="metric-label">
                    🎯 FINAL JOB MATCH
                </div>

                <div class="metric-value">
                    {final_score}%
                </div>

            </div>
            """)

        with col2:

            render_html(f"""
            <div class="metric-card">

                <div class="metric-label">
                    🔑 KEYWORD MATCH
                </div>

                <div class="metric-value">
                    {keyword_score}%
                </div>

            </div>
            """)

        with col3:

            render_html(f"""
            <div class="metric-card">

                <div class="metric-label">
                    🧠 SEMANTIC MATCH
                </div>

                <div class="metric-value">
                    {semantic_score}%
                </div>

            </div>
            """)

        with col4:

            render_html(f"""
            <div class="metric-card">

                <div class="metric-label">
                    📊 ATS SCORE
                </div>

                <div class="metric-value">
                    {ats_score}%
                </div>

            </div>
        """)

            st.progress(
                final_score / 100,
                text=f"Overall Job Compatibility — {final_score}%"
            )

            # ========================================================
            # MATCH STATUS
            # ========================================================

            render_html(f"""
            <div class="panel" style="margin-top:20px;">

                <div class="panel-title">
                    💡 Match Assessment
                </div>

                <div style="
                    font-size:18px;
                    font-weight:700;
                    color:#c7d2fe;
                    margin-top:8px;
                ">
                    {score_status}
                </div>

                <div style="
                    color:#8e99ad;
                    font-size:13px;
                    margin-top:7px;
                    line-height:1.6;
                ">
                    Your final score combines exact keyword matching
                    with AI-based semantic skill similarity.
                </div>

            </div>
            """)

            # ========================================================
            # MATCHING BREAKDOWN
            # ========================================================

            render_html("""
            <div class="section-title">
                🔍 Matching Breakdown
            </div>
            """)

            col1, col2 = st.columns(
                2,
                gap="medium"
            )

            with col1:

                render_html(f"""
                <div class="panel">

                    <div class="panel-title">
                        🔑 Keyword Matching
                    </div>

                    <div style="
                        font-size:28px;
                        font-weight:800;
                        color:#a5b4fc;
                        margin-top:10px;
                    ">
                        {keyword_score}%
                    </div>

                    <div style="
                        color:#8e99ad;
                        font-size:13px;
                        margin-top:6px;
                    ">
                        Exact skills found in both resume and job description.
                    </div>

                </div>
                """)

            with col2:

                render_html(f"""
                <div class="panel">

                    <div class="panel-title">
                        🧠 Semantic Matching
                    </div>

                    <div style="
                        font-size:28px;
                        font-weight:800;
                        color:#c084fc;
                        margin-top:10px;
                    ">
                        {semantic_score}%
                    </div>

                    <div style="
                        color:#8e99ad;
                        font-size:13px;
                        margin-top:6px;
                    ">
                        AI-based similarity between related technical skills.
                    </div>

                </div>
                """)

            # ========================================================
            # SKILL ANALYSIS
            # ========================================================

            render_html("""
            <div class="section-title">
                🧠 Skill Analysis
            </div>
            """)

            col1, col2 = st.columns(
                2,
                gap="medium"
            )

            # --------------------------------------------------------
            # SKILLS YOU HAVE
            # --------------------------------------------------------

            with col1:

                render_html("""
                <div class="panel">

                    <div class="panel-title">
                        ✅ Skills You Have
                    </div>
                """)

                if exact_matches:

                    skills_html = ""

                    for skill in exact_matches:

                        skills_html += (
                            f'<span class="skill-card">'
                            f'✓ {skill}'
                            f'</span>'
                        )

                    render_html(skills_html)

                else:

                    st.info(
                        "No exact skill matches found."
                    )

                render_html("""
                </div>
                """)

            # --------------------------------------------------------
            # MISSING SKILLS
            # --------------------------------------------------------

            with col2:

                render_html("""
                <div class="panel">

                    <div class="panel-title">
                        ⚡ Skills to Develop
                    </div>
                """)

                if missing_skills:

                    skills_html = ""

                    for skill in missing_skills:

                        skills_html += (
                            f'<span class="missing-card">'
                            f'✕ {skill}'
                            f'</span>'
                        )

                    render_html(skills_html)

                else:

                    st.success(
                        "🎉 No major skill gaps detected."
                    )

                render_html("""
                </div>
                """)

            # ========================================================
            # SEMANTIC SKILL MATCHES
            # ========================================================

            if semantic_matches:

                render_html("""
                <div class="section-title">
                    🔗 AI Semantic Skill Matches
                </div>
                """)

                render_html("""
                <div class="panel">
                """)

                for item in semantic_matches:

                    if isinstance(item, dict):

                        jd_skill = item.get(
                            "jd_skill",
                            item.get("job_skill", "Unknown")
                        )

                        resume_skill = item.get(
                            "resume_skill",
                            "Related Skill"
                        )

                        similarity = item.get(
                            "similarity",
                            0
                        )

                        render_html(f"""
                        <div style="
                            padding:12px 0;
                            border-bottom:
                                1px solid
                                rgba(255,255,255,0.06);
                        ">

                            <div style="
                                font-weight:600;
                                color:#f8fafc;
                            ">
                                {jd_skill}
                                →
                                {resume_skill}
                            </div>

                            <div style="
                                color:#a5b4fc;
                                font-size:12px;
                                margin-top:4px;
                            ">
                                Semantic similarity:
                                {round(similarity, 2)}%
                            </div>

                        </div>
                        """)

                render_html("""
                </div>
                """)

            # ========================================================
            # WEAK / RELATED MATCHES
            # ========================================================

            if weak_matches:

                render_html("""
                <div class="section-title">
                    🟡 Related Skills
                </div>
                """)

                render_html("""
                <div class="panel">
                """)

                for item in weak_matches:

                    if isinstance(item, dict):

                        jd_skill = item.get(
                            "jd_skill",
                            item.get("job_skill", "Unknown")
                        )

                        resume_skill = item.get(
                            "resume_skill",
                            "Related Skill"
                        )

                        similarity = item.get(
                            "similarity",
                            0
                        )

                        render_html(f"""
                        <div style="
                            padding:11px 0;
                            border-bottom:
                                1px solid
                                rgba(255,255,255,0.05);
                        ">

                            <div style="
                                color:#f8fafc;
                                font-weight:600;
                            ">
                                {jd_skill}
                                ↔
                                {resume_skill}
                            </div>

                            <div style="
                                color:#fbbf24;
                                font-size:12px;
                                margin-top:4px;
                            ">
                                Related match:
                                {round(similarity, 2)}%
                            </div>

                        </div>
                        """)

                render_html("""
                </div>
                """)

            # ========================================================
            # ATS ANALYSIS
            # ========================================================

            render_html("""
            <div class="section-title">
                📊 ATS Resume Analysis
            </div>
            """)

            col1, col2, col3, col4 = st.columns(
                4,
                gap="medium"
            )

            with col1:

                render_html(f"""
                <div class="metric-card">

                    <div class="metric-label">
                        ATS SCORE
                    </div>

                    <div class="metric-value">
                        {ats_result.get("ats_score", 0)}%
                    </div>

                </div>
                """)

            with col2:

                render_html(f"""
                <div class="metric-card">

                    <div class="metric-label">
                        SKILL SCORE
                    </div>

                    <div class="metric-value">
                        {ats_result.get("skill_score", 0)}%
                    </div>

                </div>
                """)

            with col3:

                render_html(f"""
                <div class="metric-card">

                    <div class="metric-label">
                        KEYWORD SCORE
                    </div>

                    <div class="metric-value">
                        {ats_result.get("keyword_score", 0)}%
                    </div>

                </div>
                """)

            with col4:

                render_html(f"""
                <div class="metric-card">

                    <div class="metric-label">
                        RESUME STRUCTURE
                    </div>

                    <div class="metric-value">
                        {ats_result.get("completeness_score", 0)}%
                    </div>

                </div>
                """)

            st.progress(
                ats_result.get("ats_score", 0) / 100,
                text=(
                    f"ATS Compatibility — "
                    f"{ats_result.get('ats_score', 0)}%"
                )
            )


        # ========================================================
        # ATS IMPROVEMENT SUGGESTIONS
        # ========================================================
        render_html("""
        <div class="section-title">
            🛠️ ATS Improvement Suggestions
        </div>
        """)

        if ats_suggestions:

            for suggestion in ats_suggestions:

                priority = suggestion["priority"]
                title = suggestion["title"]
                message = suggestion["message"]

                if priority == "High":
                    st.error(f"🔴 {priority} Priority — {title}")
                elif priority == "Medium":
                    st.warning(f"🟡 {priority} Priority — {title}")
                else:
                    st.success(f"🟢 {title}")

                st.write(message)

        else:
            st.info("No suggestions available yet.")
            # ========================================================
            # SKILL GAP PRIORITIES
            # ========================================================

            render_html("""
            <div class="section-title">
                🎯 Skill Gap Priorities
            </div>
            """)

            col1, col2 = st.columns(
                2,
                gap="medium"
            )

            with col1:

                render_html("""
                <div class="panel">

                    <div class="panel-title">
                        🔴 High Priority
                    </div>
                """)

                if skill_gap.get("high_priority"):

                    for skill in skill_gap["high_priority"]:

                        st.error(
                            f"Learn / Improve → {skill}"
                        )

                else:

                    st.success(
                        "No high-priority gaps."
                    )

                render_html("""
                </div>
                """)

            with col2:

                render_html("""
                <div class="panel">

                    <div class="panel-title">
                        🟡 Medium Priority
                    </div>
                """)

                if skill_gap.get("medium_priority"):

                    for skill in skill_gap["medium_priority"]:

                        st.warning(
                            f"Learn / Improve → {skill}"
                        )

                else:

                    st.success(
                        "No medium-priority gaps."
                    )

                render_html("""
                </div>
                """)

            # ========================================================
            # CAREER RECOMMENDATIONS
            # ========================================================

            render_html("""
            <div class="section-title">
                🚀 Career Paths For You
            </div>
            """)

            for index, recommendation in enumerate(
                career_recommendations[:6],
                start=1
            ):

                role = recommendation["role"]
                role_score = recommendation["score"]

                render_html(f"""
                <div class="career-card">

                    <div class="career-rank">
                        #{index} RECOMMENDED ROLE
                    </div>

                    <div class="career-name">
                        {role}
                    </div>

                    <div class="career-score">
                        Skill Coverage — {role_score}%
                    </div>

                </div>
                """)

                st.progress(
                    role_score / 100
                )

            # ========================================================
            # ALL RESUME SKILLS
            # ========================================================

            with st.expander(
                "🧾 View All Resume Skills"
            ):

                if resume_data["skills"]:

                    for skill in resume_data["skills"]:

                        st.write(
                            f"✓ {skill}"
                        )

                else:

                    st.info(
                        "No recognized skills were found."
                    )

            # ========================================================
            # EXTRACTED RESUME TEXT
            # ========================================================

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text(
                    resume_data["resume_text"]
                )
        # ============================================================
        # EMPTY STATE
        # ============================================================

            render_html("""
            <div class="empty-state">

                <div class="empty-icon">
                    🧭
                </div>

                <div class="empty-title">
                    Ready to discover your job fit?
                </div>

                <div class="empty-text">
                    Upload your resume, paste a job description,
                    and let JobSense AI analyze the opportunity.
                </div>

            </div>
            """)

                


        # ============================================================
        # FOOTER
        # ========================================================

        render_html("""
        <div class="footer">

            JobSense AI · Resume Intelligence & Career Matching Platform

            <br>

            Built with Python · Machine Learning · Streamlit

        </div>
        """)