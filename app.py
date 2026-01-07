# PathWise – Final Streamlit Dashboard
# AI-Assisted Career Path Explorer

import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="PathWise – Career Path Explorer",
    page_icon="🧭",
    layout="wide"
)

# =====================================================
# CSS THEME (PROFESSIONAL)
# =====================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F8FAFC;
}

.block-container {
    padding: 2rem 3rem;
}

h1 {
    color: #0F172A;
    font-weight: 800;
}

h2, h3 {
    color: #1F2937;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] button {
    background-color: #1E293B;
    border-radius: 10px;
    width: 100%;
    margin-bottom: 0.5rem;
}

.stButton > button {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #14B8A6, #0D9488);
    transform: translateY(-2px);
}

.career-card {
    background-color: white;
    padding: 1.4rem;
    border-radius: 18px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.career-card:hover {
    transform: scale(1.03);
}

.career-title {
    font-size: 1.3rem;
    font-weight: 800;
    margin-top: 0.6rem;
    color: #0F172A;
}

.career-domain {
    color: #14B8A6;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = "questionnaire"

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "selected_career" not in st.session_state:
    st.session_state.selected_career = None

# =====================================================
# LOAD DATASET
# =====================================================
@st.cache_data
def load_careers():
    return pd.read_csv("pathwise_career_dataset_300.csv")

career_df = load_careers()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## 🧭 PathWise")
    st.caption("AI-Assisted Career Path Explorer")

    st.divider()

    if st.button("🏠 Questionnaire"):
        st.session_state.page = "questionnaire"
        st.rerun()

    if st.button("🎯 Results"):
        st.session_state.page = "results"
        st.rerun()

    if st.button("🗺️ Career Roadmap"):
        if st.session_state.selected_career is not None:
            st.session_state.page = "roadmap"
            st.rerun()
        else:
            st.warning("Select a career first")

    st.divider()
    st.caption("Guidance only. Not a prediction.")

# =====================================================
# HEADER
# =====================================================
def header(title, subtitle):
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.caption(subtitle)
    st.divider()

# =====================================================
# QUESTIONNAIRE PAGE
# =====================================================
def questionnaire_page():
    header("Discover Your Career Path", "Tell us about yourself — this helps us guide you better")

    st.markdown("<p style='color:#475569;'>Select up to <b>3 options</b> where applicable for best results.</p>", unsafe_allow_html=True)

    with st.form("questionnaire"):
        st.subheader("🎓 Academic Background")
        col1, col2 = st.columns(2)

        with col1:
            education = st.selectbox(
                "Education Level",
                ["School (9–12)", "Undergraduate", "Postgraduate", "Other"]
            )
        with col2:
            field = st.selectbox(
                "Field of Study",
                ["Science", "Commerce", "Arts / Humanities", "Engineering", "Management", "Other"]
            )

        st.divider()
        st.subheader("💡 Interests & Activities")
        interests = st.multiselect(
            "Which activities do you genuinely enjoy? (Select up to 3)",
            [
                "Problem solving / logical thinking",
                "Working with numbers or data",
                "Designing or creating visuals",
                "Writing or storytelling",
                "Teaching or explaining concepts",
                "Managing people or projects",
                "Building or fixing things",
                "Researching or deep learning",
                "Public speaking or persuasion"
            ],
            max_selections=3
        )

        st.divider()
        st.subheader("💪 Strengths")
        strengths = st.multiselect(
            "What do you consider your strongest abilities? (Select up to 3)",
            [
                "Logical thinking",
                "Communication",
                "Creativity",
                "Discipline & consistency",
                "Leadership",
                "Learning new skills quickly"
            ],
            max_selections=3
        )

        st.divider()
        st.subheader("📚 Learning Preferences")
        col3, col4 = st.columns(2)

        with col3:
            learning_style = st.radio(
                "Preferred learning style",
                ["Mostly theory-based", "Mostly practical", "Balanced"]
            )
        with col4:
            learning_rate = st.radio(
                "How quickly do you usually pick up new skills?",
                ["Slow but steady", "Average", "Fast learner"]
            )

        st.divider()
        st.subheader("⏱️ Career Preferences")
        col5, col6 = st.columns(2)

        with col5:
            time_horizon = st.radio(
                "When do you want career stability?",
                ["0–1 year", "1–3 years", "3+ years"]
            )
        with col6:
            risk = st.radio(
                "Risk tolerance",
                ["Prefer stable paths", "Moderate risk", "High risk tolerance"]
            )

        submitted = st.form_submit_button("See Career Matches →")

    if submitted:
        st.session_state.profile = {
            "education": education,
            "field": field,
            "interests": interests,
            "strengths": strengths,
            "learning_style": learning_style,
            "learning_rate": learning_rate,
            "time_horizon": time_horizon,
            "risk": risk
        }
        st.session_state.page = "results"
        st.rerun()

# =====================================================
# RESULTS PAGE
# =====================================================
def results_page():
    header("Your Best Career Matches", "Top 3 paths aligned with your interests")

    user_interests = set(st.session_state.profile.get("interests", []))

    scored = []
    for _, row in career_df.iterrows():
        activities = set(row["core_activities"].split(", "))
        score = len(user_interests.intersection(activities))
        scored.append((row, score))

    top3 = sorted(scored, key=lambda x: x[1], reverse=True)[:3]

    cols = st.columns(3)

    for col, (career, _) in zip(cols, top3):
        with col:
            # Normalize career name (remove Path numbering if present)
            display_name = career['career_name'].split(' Path')[0]

            st.markdown(f"""
            <div class="career-card">
                <img src="https://source.unsplash.com/600x400/?career,profession" 
                     style="width:100%; border-radius:14px;">
                <div class="career-title">{display_name}</div>
                <div class="career-domain">{career['domain']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"View Roadmap → {display_name}"):
                st.session_state.selected_career = career
                st.session_state.selected_career['display_name'] = display_name
                st.session_state.page = "roadmap"
                st.rerun()

# =====================================================
# ROADMAP PAGE
# =====================================================
def roadmap_page():
    career = st.session_state.selected_career
    display_name = career.get('display_name', career['career_name'])

    header(display_name, "Standard Career Roadmap")

    st.subheader("📌 Overview")
    st.write(
        

    st.subheader("🛠️ Career Roadmap")
    standardized_steps = [
        "Foundation: Build subject fundamentals and core concepts",
        "Skill Development: Learn domain-specific tools and techniques",
        "Practical Exposure: Projects, internships, hands-on experience",
        "Entry Role: Apply for junior or entry-level positions",
        "Growth & Specialization: Advance to senior roles or specialize"
    ]

    for step in standardized_steps:
        st.markdown(f"- {step}")

    st.subheader("🚀 Typical Entry Roles")
    for role in career["entry_roles"].split(","):
        st.markdown(f"- {role}")

    st.subheader("🔁 Related Career Options")
    for adj in career["adjacent_careers"].split(","):
        st.markdown(f"- {adj}")

    if st.button("← Back to Results"):
        st.session_state.page = "results"
        st.rerun()

# =====================================================
# ROUTER
# =====================================================
if st.session_state.page == "questionnaire":
    questionnaire_page()
elif st.session_state.page == "results":
    results_page()
elif st.session_state.page == "roadmap":
    roadmap_page()
