import streamlit as st
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ================= PAGE ================= */

.stApp {
    background-color: #f7f7f5;
    color: #222222;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* ================= HEADINGS ================= */

.main-title {
    font-family: Georgia, serif;
    font-size: 38px;
    font-weight: 700;
    color: #222222;
    line-height: 1.2;
    margin-bottom: 12px;
}

.subtitle {
    color: #777777;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 30px;
}

.section-title {
    color: #6d5dfc;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 25px;
    margin-bottom: 15px;
}


/* ================= INPUT LABELS ================= */

label {
    color: #333333 !important;
    font-weight: 600 !important;
}


/* ================= INPUTS ================= */

.stTextInput input,
.stTextArea textarea {

    background-color: white !important;

    color: #222222 !important;

    border: 1px solid #dddddd !important;

    border-radius: 8px !important;

    padding: 11px !important;

    font-size: 14px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 1px solid #6d5dfc !important;

    box-shadow: 0 0 0 2px rgba(109,93,252,0.10) !important;
}


/* ================= SELECT BOX ================= */

.stSelectbox > div > div {

    background-color: white !important;

    color: #222222 !important;

    border: 1px solid #dddddd !important;

    border-radius: 8px !important;
}


/* ================= BUTTON ================= */

.stButton > button {

    width: 100%;

    height: 48px;

    margin-top: 12px;

    border: 1px solid #6d5dfc;

    border-radius: 8px;

    background-color: #6d5dfc;

    color: white;

    font-size: 14px;

    font-weight: 700;

    transition: 0.2s;
}

.stButton > button:hover {

    background-color: #5948e8;

    border-color: #5948e8;

    transform: translateY(-1px);
}


/* ================= RIGHT SIDE ================= */

.right-content {

    padding: 5px 20px 20px 40px;
}


/* ================= CANDIDATE ================= */

.candidate-name {

    font-family: Georgia, serif;

    font-size: 32px;

    font-weight: 700;

    color: #222222;

    margin-bottom: 5px;
}

.candidate-info {

    color: #777777;

    font-size: 14px;
}


/* ================= STATUS ================= */

.status {

    display: inline-block;

    padding: 7px 14px;

    border-radius: 20px;

    background-color: #eeeaff;

    color: #5a49d6;

    font-size: 12px;

    font-weight: 700;
}


/* ================= SCORE ================= */

.score-area {

    margin-top: 25px;

    margin-bottom: 25px;
}

.score {

    font-family: Georgia, serif;

    font-size: 58px;

    font-weight: 700;

    color: #222222;
}

.score-label {

    color: #888888;

    font-size: 14px;
}


/* ================= PROGRESS ================= */

.stProgress > div > div > div {

    background-color: #6d5dfc;
}

.stProgress {

    margin-bottom: 18px;
}


/* ================= SKILL TITLE ================= */

.skill-title {

    color: #333333;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-top: 30px;

    margin-bottom: 12px;
}


/* ================= SKILLS ================= */

.skill {

    display: inline-block;

    padding: 7px 12px;

    margin: 3px;

    border-radius: 20px;

    background-color: #f0f8f3;

    border: 1px solid #cde8d6;

    color: #32734a;

    font-size: 12px;

    font-weight: 600;
}

.skill-missing {

    display: inline-block;

    padding: 7px 12px;

    margin: 3px;

    border-radius: 20px;

    background-color: #fff5f2;

    border: 1px solid #f0d0c7;

    color: #b55742;

    font-size: 12px;

    font-weight: 600;
}


/* ================= RED FLAGS ================= */

.red-flag {

    background-color: #f0f8f3;

    border-left: 4px solid #56a66f;

    padding: 13px 16px;

    border-radius: 5px;

    color: #32734a;

    margin-top: 10px;

    font-size: 13px;
}

.warning {

    background-color: #fff5f2;

    border-left: 4px solid #d87961;

    padding: 13px 16px;

    border-radius: 5px;

    color: #a84d3a;

    margin-top: 10px;

    font-size: 13px;
}


/* ================= DIVIDER ================= */

hr {

    border: none;

    height: 1px;

    background-color: #e4e4e4;

    margin: 25px 0;
}


/* ================= CAPTION ================= */

.stCaption {

    color: #999999 !important;
}


/* ================= RESPONSIVE ================= */

@media (max-width: 900px) {

    .main-title {
        font-size: 30px;
    }

    .right-content {
        padding: 20px;
    }

    .score {
        font-size: 45px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================

def get_skills(text):

    return {
        skill.strip().lower()
        for skill in text.split(",")
        if skill.strip()
    }


def get_experience(resume):

    pattern = r"(\d+(?:\.\d+)?)\s*\+?\s*years?"

    match = re.search(
        pattern,
        resume.lower()
    )

    if match:
        return float(match.group(1))

    return 0


def calculate_score(
    required,
    preferred,
    resume,
    seniority
):

    resume_lower = resume.lower()

    # Find required skills
    required_found = [
        skill
        for skill in required
        if skill in resume_lower
    ]

    # Find preferred skills
    preferred_found = [
        skill
        for skill in preferred
        if skill in resume_lower
    ]

    # ---------------- SKILLS ----------------

    required_score = (
        len(required_found) / len(required) * 80
        if required
        else 0
    )

    preferred_score = (
        len(preferred_found) / len(preferred) * 20
        if preferred
        else 0
    )

    skill_score = (
        required_score +
        preferred_score
    )

    # ---------------- EXPERIENCE ----------------

    years = get_experience(resume)

    expected = {
        "Entry": 0,
        "Junior": 1,
        "Mid": 3,
        "Senior": 5,
        "Lead": 7
    }

    required_years = expected[seniority]

    if required_years == 0:

        experience_score = 100

    else:

        experience_score = min(
            100,
            (years / required_years) * 100
        )

    # ---------------- EDUCATION ----------------

    education_found = re.search(
        r"b\.?tech|bachelor|b\.?s\.?|"
        r"m\.?tech|master|"
        r"computer science|engineering",
        resume_lower
    )

    if education_found:

        education_score = 100

    else:

        education_score = 50

    # ---------------- OVERALL ----------------

    overall = (
        skill_score * 0.50
        + experience_score * 0.35
        + education_score * 0.15
    )

    return {

        "overall": round(overall),

        "skill": round(skill_score),

        "experience": round(experience_score),

        "education": round(education_score),

        "years": years,

        "required_found": required_found,

        "preferred_found": preferred_found
    }


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [1, 1],
    gap="large"
)


# ============================================================
# LEFT SIDE
# ============================================================

with left:

    st.markdown(
        '<div class="main-title">'
        'Screen a candidate<br>'
        'against the role'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Describe the opening, paste a resume, '
        'and get an instant candidate-fit analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------- OPENING ----------------

    st.markdown(
        '<div class="section-title">'
        'THE OPENING'
        '</div>',
        unsafe_allow_html=True
    )

    job_title = st.text_input(
        "Job title",
        "Backend Engineer"
    )

    department = st.text_input(
        "Department",
        "Engineering"
    )

    seniority = st.selectbox(
        "Seniority level",
        [
            "Entry",
            "Junior",
            "Mid",
            "Senior",
            "Lead"
        ],
        index=2
    )

    required_text = st.text_input(
        "Required skills",
        "python, sql, aws, docker"
    )

    preferred_text = st.text_input(
        "Preferred skills",
        "kubernetes, react"
    )

    # ---------------- RESUME ----------------

    st.markdown(
        '<div class="section-title">'
        'THE RESUME'
        '</div>',
        unsafe_allow_html=True
    )

    resume = st.text_area(
        "Paste resume text",
        """Jane Doe
jane.doe@email.com
555-123-4567

5 years of experience in backend development
using Python, SQL, AWS and Docker.

B.S. in Computer Science.""",
        height=190
    )

    st.caption(
        "No file upload needed — resume text is parsed directly."
    )

    screen = st.button(
        "SCREEN CANDIDATE"
    )


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.markdown(
        '<div class="right-content">',
        unsafe_allow_html=True
    )

    # ---------------- INPUT DATA ----------------

    required = get_skills(
        required_text
    )

    preferred = get_skills(
        preferred_text
    )

    result = calculate_score(
        required,
        preferred,
        resume,
        seniority
    )

    # ---------------- NAME ----------------

    lines = resume.strip().splitlines()

    if lines:

        candidate_name = lines[0]

    else:

        candidate_name = "Candidate"

    # ---------------- EMAIL ----------------

    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        resume
    )

    if email_match:

        email = email_match.group()

    else:

        email = "candidate@email.com"

    # ---------------- STATUS ----------------

    if result["overall"] >= 80:

        status = "Strong Fit"

    elif result["overall"] >= 60:

        status = "Review"

    else:

        status = "Low Match"


    # ========================================================
    # CANDIDATE INFORMATION
    # ========================================================

    header1, header2 = st.columns(
        [3, 1]
    )

    with header1:

        st.markdown(
            f'<div class="candidate-name">'
            f'{candidate_name}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="candidate-info">'
            f'{email}'
            f'</div>',
            unsafe_allow_html=True
        )

    with header2:

        st.markdown(
            f'<div class="status">'
            f'{status}'
            f'</div>',
            unsafe_allow_html=True
        )


    st.markdown("<hr>", unsafe_allow_html=True)


    # ========================================================
    # SCORE
    # ========================================================

    st.markdown(
        '<div class="score-area">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<span class="score">'
        f'{result["overall"]}'
        f'</span>'
        f'<span class="score-label">'
        f' / 100 overall fit'
        f'</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.progress(
        result["skill"] / 100,
        text=f"Skills Match                 {result['skill']}/100"
    )

    st.progress(
        result["experience"] / 100,
        text=f"Experience                  {result['experience']}/100"
    )

    st.progress(
        result["education"] / 100,
        text=f"Education                    {result['education']}/100"
    )


    # ========================================================
    # SKILLS
    # ========================================================

    st.markdown(
        '<div class="skill-title">'
        'SKILLS FOUND VS. REQUIRED'
        '</div>',
        unsafe_allow_html=True
    )


    # Required skills

    for skill in sorted(required):

        if skill in result["required_found"]:

            st.markdown(
                f'<span class="skill">'
                f'✓ {skill}'
                f'</span>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<span class="skill-missing">'
                f'✕ {skill}'
                f'</span>',
                unsafe_allow_html=True
            )


    # Preferred skills

    for skill in sorted(preferred):

        if skill in result["preferred_found"]:

            st.markdown(
                f'<span class="skill">'
                f'✓ {skill}'
                f'</span>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<span class="skill-missing">'
                f'{skill}'
                f'</span>',
                unsafe_allow_html=True
            )


    # ========================================================
    # RED FLAGS
    # ========================================================

    st.markdown(
        '<div class="skill-title">'
        'RED FLAGS'
        '</div>',
        unsafe_allow_html=True
    )


    missing = [
        skill
        for skill in required
        if skill not in result["required_found"]
    ]


    if not missing:

        st.markdown(
            '<div class="red-flag">'
            '✓ No red flags detected'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="warning">'
            '⚠ Missing required skills: '
            + ", ".join(missing)
            + '</div>',
            unsafe_allow_html=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )