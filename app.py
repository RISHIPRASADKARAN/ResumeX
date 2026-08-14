
import streamlit as st

from src.resume_parser import (
    extract_text_from_pdf,
    get_resume_statistics,
)

from src.skill_extractor import (
    extract_skills,
    compare_skills,
)

from src.job_matcher import (
    calculate_similarity,
    calculate_skill_score,
    calculate_final_score,
    get_match_category,
)

from src.recommendations import (
    generate_recommendations,
    get_resume_quality_score,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeX | AI Resume Analyzer",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# NETFLIX-STYLE CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================
   GLOBAL
   ========================= */

.stApp {
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(229, 9, 20, 0.16),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #080808 0%,
            #0b0b0b 45%,
            #111111 100%
        );

    color: #ffffff;
}

.block-container {
    max-width: 1450px;
    padding-top: 0.8rem;
    padding-bottom: 4rem;
}


/* =========================
   REMOVE STREAMLIT TOP BAR
   ========================= */

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}


/* =========================
   NAVIGATION
   ========================= */

.navbar {
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 18px;
    margin-bottom: 20px;
}

.logo {
    color: #E50914;
    font-size: 31px;
    font-weight: 900;
    letter-spacing: -1.5px;
}

.nav-right {
    color: #bdbdbd;
    font-size: 14px;
}


/* =========================
   HERO
   ========================= */

.hero {
    min-height: 440px;
    border-radius: 22px;

    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,0.96) 0%,
            rgba(0,0,0,0.84) 38%,
            rgba(0,0,0,0.35) 75%,
            rgba(0,0,0,0.75) 100%
        ),
        radial-gradient(
            circle at 75% 40%,
            rgba(229,9,20,0.45),
            transparent 35%
        ),
        #151515;

    border: 1px solid #252525;

    display: flex;
    align-items: center;

    padding: 65px;
    margin-bottom: 35px;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.45);
}

.hero-content {
    max-width: 760px;
}

.hero-tag {
    color: #E50914;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    color: #ffffff;
    font-size: 58px;
    line-height: 1.02;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 20px;
}

.hero-description {
    color: #c7c7c7;
    font-size: 18px;
    line-height: 1.65;
    max-width: 680px;
}


/* =========================
   SECTION TITLES
   ========================= */

.section-title {
    color: #ffffff;
    font-size: 25px;
    font-weight: 800;
    margin-top: 38px;
    margin-bottom: 18px;
}


/* =========================
   FEATURE CARDS
   ========================= */

.feature-card {
    background: #181818;
    border: 1px solid #292929;
    border-radius: 14px;
    padding: 24px;
    min-height: 145px;
    transition: 0.2s ease;
}

.feature-card:hover {
    border-color: #E50914;
    transform: translateY(-2px);
}

.feature-number {
    color: #E50914;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
}

.feature-title {
    color: #ffffff;
    font-size: 19px;
    font-weight: 750;
    margin-top: 10px;
    margin-bottom: 8px;
}

.feature-text {
    color: #929292;
    font-size: 14px;
    line-height: 1.5;
}


/* =========================
   INPUT CARDS
   ========================= */

.input-card {
    background: #181818;
    border: 1px solid #292929;
    border-radius: 15px;
    padding: 24px;
    min-height: 250px;
}

.input-title {
    color: #ffffff;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 6px;
}

.input-description {
    color: #888888;
    font-size: 13px;
    margin-bottom: 15px;
}


/* =========================
   STREAMLIT INPUTS
   ========================= */

.stTextArea textarea {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
}

.stTextArea textarea:focus {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 1px #E50914 !important;
}

[data-testid="stFileUploader"] {
    background: #111111;
    border: 1px dashed #444444;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stFileUploader"]:hover {
    border-color: #E50914;
}


/* =========================
   BUTTON
   ========================= */

.stButton > button {
    background: #E50914 !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    height: 54px !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #b20710 !important;
    border: none !important;
    transform: scale(1.01);
}


/* =========================
   RESULT HERO
   ========================= */

.result-panel {
    background:
        linear-gradient(
            135deg,
            #1c1c1c,
            #111111
        );

    border: 1px solid #303030;
    border-radius: 18px;
    padding: 32px;
    margin-top: 35px;
    margin-bottom: 25px;
}

.result-label {
    color: #999999;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-score {
    color: #E50914;
    font-size: 72px;
    font-weight: 900;
    line-height: 1;
    margin-top: 10px;
}

.result-category {
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    margin-top: 12px;
}


/* =========================
   METRIC CARDS
   ========================= */

.metric-card {
    background: #181818;
    border: 1px solid #292929;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
}

.metric-label {
    color: #888888;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: 850;
    margin-top: 8px;
}


/* =========================
   SKILL CARDS
   ========================= */

.skill-card {
    display: inline-block;
    background: #222222;
    border: 1px solid #333333;
    color: #eeeeee;
    padding: 8px 13px;
    border-radius: 20px;
    margin: 4px;
    font-size: 13px;
}

.missing-card {
    display: inline-block;
    background: rgba(229,9,20,0.10);
    border: 1px solid rgba(229,9,20,0.45);
    color: #ff6b70;
    padding: 8px 13px;
    border-radius: 20px;
    margin: 4px;
    font-size: 13px;
}


/* =========================
   RECOMMENDATIONS
   ========================= */

.recommendation {
    background: #181818;
    border-left: 3px solid #E50914;
    border-radius: 8px;
    padding: 17px 20px;
    margin-bottom: 10px;
    color: #cfcfcf;
    line-height: 1.5;
}


/* =========================
   FOOTER
   ========================= */

.footer {
    text-align: center;
    color: #555555;
    font-size: 13px;
    padding-top: 60px;
    padding-bottom: 20px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# NAVBAR
# =========================================================

st.markdown(
    """
<div class="navbar">
    <div class="logo">RESUMEX</div>
    <div class="nav-right">
        AI Resume Intelligence
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.html("""
<div class="hero">
    <div class="hero-content">

        <div class="hero-tag">
            AI POWERED RESUME ANALYSIS
        </div>

        <div class="hero-title">
            Find out how well your resume fits the job.
        </div>

        <div class="hero-description">
            Upload your resume and compare it with a target
            job description. ResumeX analyzes your skills,
            evaluates job compatibility and identifies the
            areas you should improve before applying.
        </div>

    </div>
</div>
""")
# =========================================================
# FEATURES
# =========================================================

st.markdown(
    '<div class="section-title">What you can do</div>',
    unsafe_allow_html=True,
)

feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.markdown(
        """
<div class="feature-card">
    <div class="feature-number">01</div>
    <div class="feature-title">Analyze Resume</div>
    <div class="feature-text">
        Extract resume content and automatically identify
        technical skills from your PDF.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

with feature2:
    st.markdown(
        """
<div class="feature-card">
    <div class="feature-number">02</div>
    <div class="feature-title">Match Jobs</div>
    <div class="feature-text">
        Compare your resume with a target role using
        TF-IDF and cosine similarity.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

with feature3:
    st.markdown(
        """
<div class="feature-card">
    <div class="feature-number">03</div>
    <div class="feature-title">Find Skill Gaps</div>
    <div class="feature-text">
        Discover matching skills, missing skills and
        personalized improvement recommendations.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# INPUT
# =========================================================

st.markdown(
    '<div class="section-title">Start your analysis</div>',
    unsafe_allow_html=True,
)

input1, input2 = st.columns(
    [1, 1],
    gap="large",
)


with input1:

    st.markdown(
        """
<div class="input-card">

<div class="input-title">
Upload your resume
</div>

<div class="input-description">
PDF format recommended
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.success(
            f"Uploaded: {uploaded_file.name}"
        )


with input2:

    st.markdown(
        """
<div class="input-card">

<div class="input-title">
Target job description
</div>

<div class="input-description">
Paste the job description you want to analyze
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    job_description = st.text_area(
        "Job Description",
        height=150,
        label_visibility="collapsed",
        placeholder=(
            "Paste the complete job description here..."
        ),
    )


st.markdown("")

analyze_button = st.button(
    "ANALYZE RESUME",
    type="primary",
    use_container_width=True,
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if uploaded_file is None:

        st.error(
            "Please upload your resume."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        with st.spinner(
            "Analyzing your resume..."
        ):

            try:

                resume_text = extract_text_from_pdf(
                    uploaded_file
                )

                if not resume_text:

                    st.error(
                        "No readable text was found in this PDF."
                    )

                    st.stop()

                resume_stats = get_resume_statistics(
                    resume_text
                )

                resume_skills = extract_skills(
                    resume_text
                )

                job_skills = extract_skills(
                    job_description
                )

                skill_comparison = compare_skills(
                    resume_skills,
                    job_skills,
                )

                similarity_score = calculate_similarity(
                    resume_text,
                    job_description,
                )

                skill_score = calculate_skill_score(
                    resume_skills,
                    job_skills,
                )

                final_score = calculate_final_score(
                    similarity_score,
                    skill_score,
                )

                match_category = get_match_category(
                    final_score
                )

                recommendations = generate_recommendations(
                    skill_comparison["missing_skills"],
                    final_score,
                    resume_text,
                )

                resume_quality = get_resume_quality_score(
                    resume_text,
                    len(resume_skills),
                )

                st.session_state["results"] = {
                    "resume_text": resume_text,
                    "resume_stats": resume_stats,
                    "resume_skills": resume_skills,
                    "job_skills": job_skills,
                    "matched_skills": skill_comparison[
                        "matched_skills"
                    ],
                    "missing_skills": skill_comparison[
                        "missing_skills"
                    ],
                    "additional_skills": skill_comparison[
                        "additional_skills"
                    ],
                    "similarity_score": similarity_score,
                    "skill_score": skill_score,
                    "final_score": final_score,
                    "match_category": match_category,
                    "recommendations": recommendations,
                    "resume_quality": resume_quality,
                }

                st.success(
                    "Analysis completed."
                )

            except Exception as error:

                st.error(
                    f"Analysis failed: {error}"
                )


# =========================================================
# RESULTS
# =========================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    st.markdown(
        '<div class="section-title">Your Match</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # MAIN RESULT
    # -----------------------------------------

    st.markdown(
        f"""
<div class="result-panel">

<div class="result-label">
Overall job compatibility
</div>

<div class="result-score">
{results["final_score"]}%
</div>

<div class="result-category">
{results["match_category"]}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


    # -----------------------------------------
    # PROGRESS
    # -----------------------------------------

    st.progress(
        min(
            results["final_score"] / 100,
            1.0
        )
    )


    # -----------------------------------------
    # METRICS
    # -----------------------------------------

    st.markdown(
        '<div class="section-title">Score breakdown</div>',
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.markdown(
            f"""
<div class="metric-card">

<div class="metric-label">
NLP Similarity
</div>

<div class="metric-value">
{results["similarity_score"]}%
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with metric2:

        st.markdown(
            f"""
<div class="metric-card">

<div class="metric-label">
Skill Match
</div>

<div class="metric-value">
{results["skill_score"]}%
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with metric3:

        st.markdown(
            f"""
<div class="metric-card">

<div class="metric-label">
Resume Quality
</div>

<div class="metric-value">
{results["resume_quality"]}%
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # -----------------------------------------
    # MATCHED / MISSING
    # -----------------------------------------

    st.markdown(
        '<div class="section-title">Skill analysis</div>',
        unsafe_allow_html=True,
    )

    skills1, skills2 = st.columns(2)

    with skills1:

        st.subheader("Matched skills")

        if results["matched_skills"]:

            html = ""

            for skill in results["matched_skills"]:

                html += (
                    f'<span class="skill-card">'
                    f'{skill}</span>'
                )

            st.markdown(
                html,
                unsafe_allow_html=True,
            )

        else:

            st.write(
                "No matching skills detected."
            )


    with skills2:

        st.subheader("Missing skills")

        if results["missing_skills"]:

            html = ""

            for skill in results["missing_skills"]:

                html += (
                    f'<span class="missing-card">'
                    f'{skill}</span>'
                )

            st.markdown(
                html,
                unsafe_allow_html=True,
            )

        else:

            st.success(
                "No missing skills detected."
            )


    # -----------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------

    st.markdown(
        '<div class="section-title">Recommendations</div>',
        unsafe_allow_html=True,
    )

    for recommendation in results["recommendations"]:

        st.markdown(
            f"""
<div class="recommendation">
{recommendation}
</div>
""",
            unsafe_allow_html=True,
        )


    # -----------------------------------------
    # RESUME STATISTICS
    # -----------------------------------------

    st.markdown(
        '<div class="section-title">Resume overview</div>',
        unsafe_allow_html=True,
    )

    stat1, stat2, stat3 = st.columns(3)

    with stat1:

        st.metric(
            "Words",
            results["resume_stats"]["words"],
        )

    with stat2:

        st.metric(
            "Characters",
            results["resume_stats"]["characters"],
        )

    with stat3:

        st.metric(
            "Detected Skills",
            len(results["resume_skills"]),
        )


    # -----------------------------------------
    # ALL SKILLS
    # -----------------------------------------

    with st.expander(
        "View all detected resume skills"
    ):

        if results["resume_skills"]:

            st.write(
                ", ".join(
                    results["resume_skills"]
                )
            )

        else:

            st.write(
                "No skills detected."
            )


    # -----------------------------------------
    # EXTRACTED TEXT
    # -----------------------------------------

    with st.expander(
        "View extracted resume text"
    ):

        st.text(
            results["resume_text"]
        )


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">
    RESUMEX • AI Resume Analyzer & Job Matcher
    <br>
    Created by <strong>Rishi Prasad Karan</strong>
    <br>
    Built with Python • NLP • Scikit-learn • Streamlit
</div>
""")