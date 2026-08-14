import re
from io import BytesIO

import streamlit as st

# Optional document readers
try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

# NLP
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:
    TfidfVectorizer = None
    cosine_similarity = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeX | AI Resume Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# NETFLIX STYLE / RESUMEX CSS
# ============================================================

st.markdown(
    """
<style>
/* ---------- GLOBAL ---------- */
html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 82% 8%, rgba(229, 9, 20, 0.12), transparent 30%),
        linear-gradient(180deg, #080808 0%, #0a0a0a 45%, #080808 100%) !important;
    color: #e5e5e5 !important;
}

.main .block-container {
    max-width: 1660px !important;
    padding: 0 5.5rem 5rem !important;
}

/* ---------- HIDE STREAMLIT CHROME ---------- */
#MainMenu,
footer,
header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

/* ---------- TOP NAV ---------- */
.resumex-nav {
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    margin-bottom: 30px;
}

.resumex-logo {
    color: #e50914 !important;
    font-size: 40px !important;
    font-weight: 900 !important;
    letter-spacing: -2px;
}

.resumex-tagline {
    color: #b3b3b3 !important;
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* ---------- TEXT ---------- */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

p, span, label, div {
    color: #d8d8d8;
}

.section-title {
    color: #ffffff !important;
    font-size: 34px;
    font-weight: 800;
    margin: 55px 0 25px;
    letter-spacing: -0.7px;
}

/* ---------- HERO ---------- */
.hero {
    min-height: 560px;
    border: 1px solid #292929;
    border-radius: 30px;
    padding: 115px 95px 90px;
    background:
        radial-gradient(circle at 75% 35%, rgba(229, 9, 20, 0.28), transparent 34%),
        linear-gradient(110deg, #000000 0%, #050505 54%, #220305 100%);
    box-shadow: 0 20px 80px rgba(0, 0, 0, 0.45);
    overflow: hidden;
}

.hero-kicker {
    color: #e50914 !important;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 5px;
    margin-bottom: 28px;
}

.hero-title {
    color: #ffffff !important;
    font-size: clamp(52px, 5vw, 82px);
    line-height: 0.98;
    font-weight: 900;
    letter-spacing: -3px;
    max-width: 1080px;
    margin: 0 0 38px;
}

.hero-copy {
    color: #bcbcbc !important;
    font-size: 23px;
    line-height: 1.55;
    max-width: 1080px;
}

/* ---------- INPUT AREA ---------- */
.input-card {
    background: #111111;
    border: 1px solid #292929;
    border-radius: 20px;
    padding: 28px;
    margin-top: 28px;
}

.input-label {
    color: #ffffff !important;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* ---------- STREAMLIT INPUTS ---------- */
textarea,
input {
    color: #ffffff !important;
    background: #111111 !important;
    border: 1px solid #3b3b3b !important;
    border-radius: 12px !important;
}

textarea:focus,
input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 1px #e50914 !important;
}

textarea::placeholder,
input::placeholder {
    color: #777777 !important;
}

[data-testid="stFileUploader"] {
    background: #111111 !important;
    border: 1px solid #292929 !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #d8d8d8 !important;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border: 0 !important;
    border-radius: 10px !important;
    background: #e50914 !important;
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    transition: 0.2s ease !important;
}

.stButton > button:hover {
    background: #b20710 !important;
    color: #ffffff !important;
    transform: translateY(-1px);
}

.stButton > button:focus {
    color: #ffffff !important;
    box-shadow: 0 0 0 2px rgba(229, 9, 20, 0.35) !important;
}

/* ---------- MATCH CARD ---------- */
.match-card {
    background:
        radial-gradient(circle at 78% 20%, rgba(229, 9, 20, 0.10), transparent 28%),
        #171717;
    border: 1px solid #303030;
    border-radius: 22px;
    padding: 52px 48px;
}

.metric-label {
    color: #999999 !important;
    font-size: 18px;
    letter-spacing: 4px;
    font-weight: 500;
}

.metric-score {
    color: #e50914 !important;
    font-size: 96px;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -4px;
    margin: 20px 0 30px;
}

.match-status {
    color: #ffffff !important;
    font-size: 27px;
    font-weight: 800;
}

/* ---------- RED PROGRESS ---------- */
div[data-testid="stProgress"] > div {
    background: #292929 !important;
    border-radius: 999px !important;
}

div[data-testid="stProgress"] > div > div {
    background: #e50914 !important;
    border-radius: 999px !important;
}

div[data-testid="stProgress"] [role="progressbar"] {
    background-color: #e50914 !important;
}

/* ---------- SCORE BREAKDOWN ---------- */
.score-card {
    background: #181818;
    border: 1px solid #303030;
    border-radius: 18px;
    padding: 36px 20px;
    text-align: center;
    min-height: 170px;
}

.score-card-title {
    color: #999999 !important;
    font-size: 17px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 22px;
}

.score-card-value {
    color: #ffffff !important;
    font-size: 42px;
    font-weight: 900;
}

/* ---------- SKILLS ---------- */
.skill-section-title {
    color: #ffffff !important;
    font-size: 38px;
    font-weight: 700;
    margin: 10px 0 24px;
}

.skill-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: flex-start;
}

.skill-badge {
    display: inline-block;
    color: #dedede !important;
    background: #222222 !important;
    border: 1px solid #393939 !important;
    border-radius: 999px;
    padding: 13px 20px;
    font-size: 16px;
    line-height: 1;
}

.missing-skill {
    display: inline-block;
    color: #ff5a5f !important;
    background: #170707 !important;
    border: 1px solid #e50914 !important;
    border-radius: 999px;
    padding: 13px 20px;
    font-size: 16px;
    line-height: 1;
}

/* ---------- RECOMMENDATIONS ---------- */
.recommendation {
    background: #181818 !important;
    border-left: 4px solid #e50914 !important;
    border-radius: 12px;
    padding: 23px 28px;
    margin: 14px 0;
    color: #d8d8d8 !important;
    font-size: 17px;
    line-height: 1.5;
}

.recommendation * {
    color: #d8d8d8 !important;
}

/* ---------- EXPANDER ---------- */
[data-testid="stExpander"] {
    background: #111111 !important;
    border: 1px solid #292929 !important;
    border-radius: 14px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #ffffff !important;
}

/* ---------- ALERTS ---------- */
[data-testid="stAlert"] {
    background: #151515 !important;
    color: #e5e5e5 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #e5e5e5 !important;
}

/* ---------- MOBILE ---------- */
@media (max-width: 900px) {
    .main .block-container {
        padding: 0 1.2rem 3rem !important;
    }

    .resumex-nav {
        padding: 0;
        height: 80px;
    }

    .resumex-logo {
        font-size: 30px !important;
    }

    .resumex-tagline {
        font-size: 14px !important;
    }

    .hero {
        padding: 65px 30px;
        min-height: auto;
    }

    .hero-title {
        font-size: 48px;
        letter-spacing: -2px;
    }

    .hero-copy {
        font-size: 18px;
    }

    .metric-score {
        font-size: 70px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": [" c ", "c programming", "c language"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node js"],
    "php": ["php"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "rest api": ["rest api", "restful api", "restful"],
    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "data science": ["data science"],
    "data analytics": ["data analytics", "data analysis"],
    "data engineering": ["data engineering"],
    "computer vision": ["computer vision"],
    "natural language processing": ["natural language processing", "nlp"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "streamlit": ["streamlit"],
    "statistics": ["statistics", "statistical analysis"],
    "excel": ["excel", "microsoft excel"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux"],
    "spring": ["spring", "spring boot"],
    "oop": ["object oriented programming", "oop", "oops"],
    "dsa": ["data structures", "data structures and algorithms", "dsa"],
}

# Words that commonly appear in job descriptions but are not useful as skills
STOP_SKILL_WORDS = {
    "and", "or", "the", "with", "for", "from", "this", "that", "have",
    "has", "are", "will", "you", "your", "our", "their", "into", "using",
    "years", "year", "experience", "work", "working", "team", "skills",
    "role", "job", "knowledge", "ability", "strong", "good", "excellent",
}


def clean_text(text: str) -> str:
    text = text or ""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_pdf(uploaded_file) -> str:
    if PdfReader is None:
        return ""

    try:
        data = uploaded_file.getvalue()
        reader = PdfReader(BytesIO(data))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return clean_text("\n".join(pages))
    except Exception:
        return ""


def extract_docx(uploaded_file) -> str:
    if Document is None:
        return ""

    try:
        data = uploaded_file.getvalue()
        document = Document(BytesIO(data))
        paragraphs = [p.text for p in document.paragraphs]
        return clean_text("\n".join(paragraphs))
    except Exception:
        return ""


def extract_resume_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_pdf(uploaded_file)

    if name.endswith(".docx"):
        return extract_docx(uploaded_file)

    if name.endswith(".txt"):
        try:
            return clean_text(uploaded_file.getvalue().decode("utf-8", errors="ignore"))
        except Exception:
            return ""

    return ""


def contains_skill(text: str, alias: str) -> bool:
    text_lower = f" {text.lower()} "

    # Keep phrases such as "c++" and "c#" safe.
    if alias in {" c ", "c programming", "c language"}:
        return bool(re.search(r"(?<![a-z])c(?![a-z+#])", text_lower))

    if alias in {"c++", "cpp"}:
        return "c++" in text_lower or "cpp" in text_lower

    pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text_lower))


def detect_skills(text: str):
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_skill(text, alias) for alias in aliases):
            found.append(skill)

    return found


def calculate_nlp_similarity(resume_text: str, job_description: str) -> float:
    if not resume_text or not job_description:
        return 0.0

    if TfidfVectorizer is None or cosine_similarity is None:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=7000,
        )
        matrix = vectorizer.fit_transform([resume_text, job_description])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100
        return round(max(0.0, min(100.0, score)), 2)
    except Exception:
        return 0.0


def calculate_skill_match(resume_text: str, job_description: str):
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_description)

    if not job_skills:
        return 0.0, resume_skills, []

    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]

    score = (len(matched) / len(job_skills)) * 100
    return round(score, 2), matched, missing


def calculate_resume_quality(text: str) -> int:
    """
    Simple resume-quality score based on useful structural signals.
    This is intentionally transparent and does not pretend to be an
    external ATS score.
    """
    if not text:
        return 0

    score = 0
    lower = text.lower()

    # Length
    word_count = len(text.split())
    if word_count >= 250:
        score += 20
    elif word_count >= 150:
        score += 15
    elif word_count >= 80:
        score += 10

    # Common sections
    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certification",
        "summary",
        "objective",
    ]
    section_hits = sum(1 for section in sections if section in lower)
    score += min(35, section_hits * 5)

    # Contact/profile signals
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", text):
        score += 10

    if re.search(r"(linkedin\.com|github\.com)", lower):
        score += 10

    if re.search(r"\b\d{10}\b", re.sub(r"\D", "", text)):
        score += 5

    # Achievement / measurable-result signals
    measurable = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:%|percent|x|k|m|million|thousand)?\b",
        text,
        flags=re.I,
    )
    score += min(15, len(measurable) * 3)

    # Action verbs
    action_verbs = [
        "developed", "built", "created", "designed", "implemented",
        "analyzed", "improved", "managed", "automated", "deployed",
        "led", "optimized", "tested", "integrated",
    ]
    action_hits = sum(1 for verb in action_verbs if verb in lower)
    score += min(15, action_hits * 2)

    return int(min(100, score))


def calculate_overall(nlp_score: float, skill_score: float, quality_score: int) -> float:
    # Job fit is weighted more heavily than formatting quality.
    overall = (nlp_score * 0.35) + (skill_score * 0.50) + (quality_score * 0.15)
    return round(max(0.0, min(100.0, overall)), 2)


def status_text(score: float) -> str:
    if score >= 80:
        return "Excellent Match"
    if score >= 65:
        return "Strong Match"
    if score >= 50:
        return "Moderate Match"
    if score >= 35:
        return "Low Match"
    return "Very Low Match"


def make_recommendations(
    overall: float,
    missing_skills,
    quality_score: int,
    resume_text: str,
):
    recommendations = []

    if missing_skills:
        shown = ", ".join(missing_skills[:8])
        recommendations.append(
            f"Consider adding or developing these required skills: {shown}."
        )

    if len(missing_skills) >= 3:
        recommendations.append(
            "Your resume is missing several skills from the job description. "
            "Prioritize the most frequently requested skills before applying."
        )

    if overall < 60:
        recommendations.append(
            "Your current resume has a relatively low match with this role. "
            "Review the job description and tailor your resume to the required technologies."
        )

    lower = resume_text.lower()

    if "linkedin.com" not in lower:
        recommendations.append(
            "Add your LinkedIn profile to make your professional profile easier to verify."
        )

    if not re.search(r"\b\d+(?:\.\d+)?\s*(?:%|percent|x|million|k|m)\b", resume_text, re.I):
        recommendations.append(
            "Use measurable results where possible, such as percentages, project performance, "
            "processing time, or accuracy."
        )

    if quality_score < 60:
        recommendations.append(
            "Improve resume structure by keeping clear sections for education, experience, "
            "projects, and technical skills."
        )

    if not recommendations:
        recommendations.append(
            "Your resume is well aligned with the role. Keep the wording targeted and "
            "support your strongest claims with measurable results."
        )

    return recommendations


def render_skills(skills, missing=False):
    if not skills:
        text = "No skills detected."
        return f'<span class="{"missing-skill" if missing else "skill-badge"}">{text}</span>'

    cls = "missing-skill" if missing else "skill-badge"
    return "".join(
        f'<span class="{cls}">{skill}</span>' for skill in skills
    )


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    """
<div class="resumex-nav">
    <div class="resumex-logo">RESUMEX</div>
    <div class="resumex-tagline">AI Resume Intelligence</div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-kicker">AI POWERED RESUME ANALYSIS</div>
    <div class="hero-title">
        Find out how well your resume<br>
        fits the job.
    </div>
    <div class="hero-copy">
        Upload your resume and compare it with a target job description.
        ResumeX analyzes your skills, evaluates job compatibility and
        identifies the areas you should improve before applying.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# INPUTS
# ============================================================

st.markdown('<div class="section-title">Analyze your resume</div>', unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="input-label">Upload your resume</div>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader(
        "Choose a PDF, DOCX or TXT file",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )

with right:
    st.markdown('<div class="input-label">Target job description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the job description",
        height=190,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
    )

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

analyze_clicked = st.button("ANALYZE RESUME", use_container_width=True)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_clicked:
    if uploaded_resume is None:
        st.error("Please upload your resume first.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste the target job description.")
        st.stop()

    resume_text = extract_resume_text(uploaded_resume)

    if not resume_text:
        st.error(
            "I could not extract readable text from this file. "
            "Try a text-based PDF, DOCX or TXT resume."
        )
        st.stop()

    nlp_score = calculate_nlp_similarity(resume_text, job_description)
    skill_score, matched_skills, missing_skills = calculate_skill_match(
        resume_text, job_description
    )
    quality_score = calculate_resume_quality(resume_text)
    overall = calculate_overall(nlp_score, skill_score, quality_score)

    st.session_state["analysis"] = {
        "resume_text": resume_text,
        "nlp_score": nlp_score,
        "skill_score": skill_score,
        "quality_score": quality_score,
        "overall": overall,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": make_recommendations(
            overall,
            missing_skills,
            quality_score,
            resume_text,
        ),
    }


# ============================================================
# RESULTS
# ============================================================

if "analysis" in st.session_state:
    data = st.session_state["analysis"]

    st.markdown('<div class="section-title">Your Match</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="match-card">
    <div class="metric-label">OVERALL JOB COMPATIBILITY</div>
    <div class="metric-score">{data["overall"]:.2f}%</div>
    <div class="match-status">{status_text(data["overall"])}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.progress(data["overall"] / 100)

    # ---------- SCORE BREAKDOWN ----------
    st.markdown('<div class="section-title">Score breakdown</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown(
            f"""
<div class="score-card">
    <div class="score-card-title">NLP Similarity</div>
    <div class="score-card-value">{data["nlp_score"]:.2f}%</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
<div class="score-card">
    <div class="score-card-title">Skill Match</div>
    <div class="score-card-value">{data["skill_score"]:.2f}%</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
<div class="score-card">
    <div class="score-card-title">Resume Quality</div>
    <div class="score-card-value">{data["quality_score"]}%</div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ---------- SKILLS ----------
    st.markdown('<div class="section-title">Skill analysis</div>', unsafe_allow_html=True)

    skill_left, skill_right = st.columns(2, gap="large")

    with skill_left:
        st.markdown(
            '<div class="skill-section-title">Matched skills</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="skill-wrap">{render_skills(data["matched_skills"])}</div>',
            unsafe_allow_html=True,
        )

    with skill_right:
        st.markdown(
            '<div class="skill-section-title">Missing skills</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="skill-wrap">{render_skills(data["missing_skills"], missing=True)}</div>',
            unsafe_allow_html=True,
        )

    # ---------- RECOMMENDATIONS ----------
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

    for recommendation in data["recommendations"]:
        st.markdown(
            f'<div class="recommendation">{recommendation}</div>',
            unsafe_allow_html=True,
        )

    # ---------- EXTRACTED RESUME ----------
    with st.expander("View extracted resume text"):
        st.markdown(
            f'<div class="resume-text">{data["resume_text"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div style="
    text-align:center;
    color:#666666;
    font-size:14px;
    margin-top:60px;
    padding-top:25px;
    border-top:1px solid #202020;
">
    ResumeX • AI Resume Intelligence
</div>
""",
        unsafe_allow_html=True,
    )
