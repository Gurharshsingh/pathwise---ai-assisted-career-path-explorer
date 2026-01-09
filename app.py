import streamlit as st
import pandas as pd
import joblib
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="PathWise – AI Career Explorer",
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
# ML MODEL LOADING & PREDICTION LOGIC
# =====================================================
@st.cache_resource
def load_ml_assets():
    try:
        model = joblib.load('career_fit_regressor.joblib')
        mlb_int = joblib.load('interests_binarizer.joblib')
        mlb_str = joblib.load('strengths_binarizer.joblib')
        features = joblib.load('model_features.joblib')
        all_careers = joblib.load('career_list.joblib')
        return model, mlb_int, mlb_str, features, all_careers
    except Exception as e:
        st.error(f"Error loading ML assets: {e}")
        return None, None, None, None, None

model, mlb_int, mlb_str, model_features, all_careers = load_ml_assets()

def get_ml_recommendations(profile):
    """Predicts fit_score and normalizes them for diverse results."""
    input_rows = []
    for career in all_careers:
        row = {
            'education': profile['education'],
            'field': profile['field'],
            'learning_rate': profile['learning_rate'],
            'time_horizon': profile['time_horizon'], # Time to Stability
            'risk_tolerance': profile['risk'],
            'career': career,
            'interests': profile['interests'],
            'strengths': profile['strengths']
        }
        input_rows.append(row)
    
    df_input = pd.DataFrame(input_rows)

    # ML Preprocessing
    int_encoded = mlb_int.transform(df_input['interests'])
    str_encoded = mlb_str.transform(df_input['strengths'])
    df_int = pd.DataFrame(int_encoded, columns=[f"interest_{c}" for c in mlb_int.classes_])
    df_str = pd.DataFrame(str_encoded, columns=[f"strength_{c}" for c in mlb_str.classes_])
    df_cat = pd.get_dummies(df_input[['education', 'field', 'learning_rate', 'time_horizon', 'risk_tolerance', 'career']])

    # Feature Alignment
    X_final = pd.concat([df_cat, df_int, df_str], axis=1)
    for col in model_features:
        if col not in X_final.columns:
            X_final[col] = 0
    X_final = X_final[model_features]

    # Predict & Normalization
    raw_scores = model.predict(X_final)
    max_raw, min_raw = np.max(raw_scores), np.min(raw_scores)
    
    results = []
    for i, career in enumerate(all_careers):
        # Stretch scores so top matches feel significant (80%+)
        norm_score = (raw_scores[i] - min_raw) / (max_raw - min_raw) if max_raw != min_raw else 0.5
        display_score = 80 + (norm_score * 15) 
        results.append({'career_name': career, 'fit_score': round(float(display_score), 1)})
    
    return sorted(results, key=lambda x: x['fit_score'], reverse=True)[:3]

# =====================================================
# INTERNAL CAREER KNOWLEDGE BASE (36 ROADMAPS)
# =====================================================
CAREER_ROADMAPS = {

    # ================================
    # Technology & Software (4)
    # ================================
    "Software Engineer": {
        "Foundation": [
            "Programming fundamentals (Python/Java)",
            "Computer science basics",
            "Problem-solving and logic"
        ],
        "Skill Building": [
            "Data Structures & Algorithms",
            "Databases and APIs",
            "Version control (Git)"
        ],
        "Entry Level": [
            "Junior Software Engineer",
            "Associate Developer",
            "Backend/Frontend Trainee"
        ],
        "Growth": [
            "Senior Engineer",
            "Tech Lead",
            "System Architect"
        ]
    },

    "Data Analyst": {
        "Foundation": [
            "Excel and data basics",
            "Statistics fundamentals",
            "Data interpretation"
        ],
        "Skill Building": [
            "SQL and Python",
            "Data visualization tools",
            "Business analytics"
        ],
        "Entry Level": [
            "Junior Data Analyst",
            "Business Analyst",
            "Reporting Analyst"
        ],
        "Growth": [
            "Senior Analyst",
            "Data Scientist",
            "Analytics Manager"
        ]
    },

    "Product Manager (Tech)": {
        "Foundation": [
            "Product lifecycle understanding",
            "Business fundamentals",
            "Communication skills"
        ],
        "Skill Building": [
            "User research",
            "Agile/Scrum methods",
            "Roadmapping tools"
        ],
        "Entry Level": [
            "Associate Product Manager",
            "Product Analyst"
        ],
        "Growth": [
            "Senior Product Manager",
            "Product Lead",
            "Head of Product"
        ]
    },

    "QA / Test Engineer": {
        "Foundation": [
            "Software testing concepts",
            "SDLC understanding",
            "Attention to detail"
        ],
        "Skill Building": [
            "Manual & automation testing",
            "Test tools (Selenium)",
            "Bug tracking systems"
        ],
        "Entry Level": [
            "QA Engineer",
            "Test Analyst"
        ],
        "Growth": [
            "Automation Lead",
            "QA Manager",
            "Release Manager"
        ]
    },

    # ================================
    # Business, Management & Operations (4)
    # ================================
    "Business Analyst": {
        "Foundation": [
            "Business fundamentals",
            "Communication skills",
            "Problem-solving"
        ],
        "Skill Building": [
            "Requirement gathering",
            "Data analysis tools",
            "Process modeling"
        ],
        "Entry Level": [
            "Junior Business Analyst",
            "Operations Analyst"
        ],
        "Growth": [
            "Senior BA",
            "Product Manager",
            "Consultant"
        ]
    },

    "Operations Manager": {
        "Foundation": [
            "Operations basics",
            "Organizational behavior",
            "Time management"
        ],
        "Skill Building": [
            "Process optimization",
            "Supply chain basics",
            "People management"
        ],
        "Entry Level": [
            "Operations Executive",
            "Process Coordinator"
        ],
        "Growth": [
            "Senior Operations Manager",
            "General Manager"
        ]
    },

    "Management Consultant": {
        "Foundation": [
            "Business strategy basics",
            "Analytical thinking",
            "Presentation skills"
        ],
        "Skill Building": [
            "Case study analysis",
            "Data-driven decision making",
            "Client communication"
        ],
        "Entry Level": [
            "Consulting Analyst",
            "Associate Consultant"
        ],
        "Growth": [
            "Senior Consultant",
            "Engagement Manager",
            "Partner"
        ]
    },

    "Entrepreneur": {
        "Foundation": [
            "Business ideation",
            "Market understanding",
            "Risk-taking mindset"
        ],
        "Skill Building": [
            "Fundraising basics",
            "Marketing and sales",
            "Team building"
        ],
        "Entry Level": [
            "Startup Founder",
            "Co-founder"
        ],
        "Growth": [
            "Scale-up Founder",
            "Serial Entrepreneur"
        ]
    },

    # ================================
    # Design, Media & Digital Creative (4)
    # ================================
    "UI/UX Designer": {
        "Foundation": [
            "Design principles",
            "User-centered thinking",
            "Visual aesthetics"
        ],
        "Skill Building": [
            "Wireframing & prototyping",
            "Figma/Adobe tools",
            "UX research"
        ],
        "Entry Level": [
            "Junior UI/UX Designer",
            "Product Designer"
        ],
        "Growth": [
            "Senior Designer",
            "Design Lead",
            "UX Manager"
        ]
    },

    "Graphic Designer": {
        "Foundation": [
            "Color theory",
            "Typography",
            "Creative thinking"
        ],
        "Skill Building": [
            "Photoshop/Illustrator",
            "Brand design",
            "Layout composition"
        ],
        "Entry Level": [
            "Graphic Designer",
            "Visual Designer"
        ],
        "Growth": [
            "Senior Designer",
            "Art Director"
        ]
    },

    "Content Strategist / Copywriter": {
        "Foundation": [
            "Writing fundamentals",
            "Storytelling",
            "Audience understanding"
        ],
        "Skill Building": [
            "SEO writing",
            "Content planning",
            "Marketing analytics"
        ],
        "Entry Level": [
            "Content Writer",
            "Copywriter"
        ],
        "Growth": [
            "Content Strategist",
            "Editorial Lead"
        ]
    },

    "Digital Media Specialist": {
        "Foundation": [
            "Media fundamentals",
            "Social platforms understanding",
            "Creativity"
        ],
        "Skill Building": [
            "Video editing",
            "Campaign analytics",
            "Content optimization"
        ],
        "Entry Level": [
            "Media Executive",
            "Social Media Manager"
        ],
        "Growth": [
            "Media Strategist",
            "Digital Marketing Head"
        ]
    },

    # ================================
    # Fashion, Architecture & Physical Design (4)
    # ================================
    "Fashion Designer": {
        "Foundation": [
            "Fashion basics",
            "Fabric knowledge",
            "Sketching"
        ],
        "Skill Building": [
            "Garment construction",
            "Trend analysis",
            "Design software"
        ],
        "Entry Level": [
            "Junior Fashion Designer"
        ],
        "Growth": [
            "Senior Designer",
            "Fashion Brand Owner"
        ]
    },

    "Textile Designer": {
        "Foundation": [
            "Textile science",
            "Pattern basics",
            "Color understanding"
        ],
        "Skill Building": [
            "Fabric design",
            "Weaving techniques",
            "CAD tools"
        ],
        "Entry Level": [
            "Textile Designer"
        ],
        "Growth": [
            "Senior Textile Designer",
            "Design Consultant"
        ]
    },

    "Architect": {
        "Foundation": [
            "Design fundamentals",
            "Engineering basics",
            "Spatial thinking"
        ],
        "Skill Building": [
            "AutoCAD/Revit",
            "Structural planning",
            "Building codes"
        ],
        "Entry Level": [
            "Junior Architect"
        ],
        "Growth": [
            "Senior Architect",
            "Principal Architect"
        ]
    },

    "Interior Designer": {
        "Foundation": [
            "Interior aesthetics",
            "Space planning",
            "Material basics"
        ],
        "Skill Building": [
            "Design software",
            "Client handling",
            "Lighting design"
        ],
        "Entry Level": [
            "Interior Designer"
        ],
        "Growth": [
            "Senior Interior Designer",
            "Design Studio Owner"
        ]
    },

    # ================================
    # Finance, Accounting & Economics (4)
    # ================================
    "Financial Analyst": {
        "Foundation": [
            "Finance basics",
            "Accounting principles",
            "Excel skills"
        ],
        "Skill Building": [
            "Financial modeling",
            "Valuation techniques",
            "Market analysis"
        ],
        "Entry Level": [
            "Junior Financial Analyst"
        ],
        "Growth": [
            "Senior Analyst",
            "Finance Manager"
        ]
    },

    "Chartered Accountant (CA)": {
        "Foundation": [
            "Accounting fundamentals",
            "Taxation basics",
            "Law basics"
        ],
        "Skill Building": [
            "Auditing",
            "Advanced taxation",
            "Compliance"
        ],
        "Entry Level": [
            "CA Articleship"
        ],
        "Growth": [
            "Practicing CA",
            "Finance Director"
        ]
    },

    "Investment Banking Analyst": {
        "Foundation": [
            "Corporate finance basics",
            "Accounting knowledge",
            "Analytical thinking"
        ],
        "Skill Building": [
            "Valuation",
            "M&A analysis",
            "Pitch deck creation"
        ],
        "Entry Level": [
            "IB Analyst"
        ],
        "Growth": [
            "Associate",
            "Vice President"
        ]
    },

    "Risk & Compliance Analyst": {
        "Foundation": [
            "Risk fundamentals",
            "Regulatory basics",
            "Ethics"
        ],
        "Skill Building": [
            "Compliance frameworks",
            "Risk modeling",
            "Audit processes"
        ],
        "Entry Level": [
            "Risk Analyst"
        ],
        "Growth": [
            "Compliance Manager",
            "Chief Risk Officer"
        ]
    },

    # ================================
    # Government, Public Service & Education (4)
    # ================================
    "Civil Services / Government Exams": {
        "Foundation": [
            "General studies",
            "Current affairs",
            "Ethics"
        ],
        "Skill Building": [
            "Answer writing",
            "Optional subject prep",
            "Mock tests"
        ],
        "Entry Level": [
            "Civil Services Officer"
        ],
        "Growth": [
            "Senior Bureaucrat",
            "Policy Maker"
        ]
    },

    "Public Sector Officer": {
        "Foundation": [
            "Public administration basics",
            "Aptitude skills",
            "General awareness"
        ],
        "Skill Building": [
            "Departmental training",
            "Policy implementation",
            "Leadership skills"
        ],
        "Entry Level": [
            "Public Sector Officer"
        ],
        "Growth": [
            "Senior Officer",
            "Department Head"
        ]
    },

    "School / College Teacher": {
        "Foundation": [
            "Subject mastery",
            "Teaching aptitude",
            "Communication"
        ],
        "Skill Building": [
            "Pedagogy",
            "Assessment techniques",
            "Curriculum planning"
        ],
        "Entry Level": [
            "Assistant Teacher",
            "Lecturer"
        ],
        "Growth": [
            "Senior Teacher",
            "Principal"
        ]
    },

    "Policy / Research Assistant": {
        "Foundation": [
            "Research methods",
            "Policy basics",
            "Analytical skills"
        ],
        "Skill Building": [
            "Data analysis",
            "Report writing",
            "Field research"
        ],
        "Entry Level": [
            "Policy Analyst"
        ],
        "Growth": [
            "Senior Researcher",
            "Policy Advisor"
        ]
    },

    # ================================
    # Healthcare & Life Sciences (4)
    # ================================
    "Medical Doctor": {
        "Foundation": [
            "Biology and anatomy",
            "Medical entrance preparation",
            "Ethics"
        ],
        "Skill Building": [
            "Clinical training",
            "Diagnosis skills",
            "Patient care"
        ],
        "Entry Level": [
            "Junior Resident"
        ],
        "Growth": [
            "Specialist Doctor",
            "Consultant"
        ]
    },

    "Dentist": {
        "Foundation": [
            "Dental sciences basics",
            "Biology fundamentals",
            "Manual dexterity"
        ],
        "Skill Building": [
            "Clinical dentistry",
            "Oral surgery basics",
            "Patient handling"
        ],
        "Entry Level": [
            "Dental Practitioner"
        ],
        "Growth": [
            "Dental Specialist",
            "Clinic Owner"
        ]
    },

    "Pharmacist": {
        "Foundation": [
            "Pharmaceutical sciences",
            "Chemistry basics",
            "Drug knowledge"
        ],
        "Skill Building": [
            "Dispensing",
            "Clinical pharmacy",
            "Regulatory compliance"
        ],
        "Entry Level": [
            "Pharmacist"
        ],
        "Growth": [
            "Clinical Pharmacist",
            "Pharma Manager"
        ]
    },

    "Public Health Professional": {
        "Foundation": [
            "Public health basics",
            "Epidemiology",
            "Statistics"
        ],
        "Skill Building": [
            "Health program planning",
            "Data analysis",
            "Policy evaluation"
        ],
        "Entry Level": [
            "Public Health Officer"
        ],
        "Growth": [
            "Program Manager",
            "Health Policy Expert"
        ]
    },

    # ================================
    # Aviation, Law & Regulated (4)
    # ================================
    "Commercial Pilot": {
        "Foundation": [
            "Physics and mathematics",
            "Aviation fundamentals",
            "Medical fitness"
        ],
        "Skill Building": [
            "Flight training",
            "Simulator practice",
            "Navigation skills"
        ],
        "Entry Level": [
            "First Officer"
        ],
        "Growth": [
            "Captain",
            "Training Pilot"
        ]
    },

    "Lawyer / Advocate": {
        "Foundation": [
            "Legal fundamentals",
            "Critical reasoning",
            "Ethics"
        ],
        "Skill Building": [
            "Case laws",
            "Drafting",
            "Court practice"
        ],
        "Entry Level": [
            "Junior Advocate"
        ],
        "Growth": [
            "Senior Advocate",
            "Legal Consultant"
        ]
    },

    "Chartered Engineer": {
        "Foundation": [
            "Engineering basics",
            "Problem solving",
            "Technical knowledge"
        ],
        "Skill Building": [
            "Professional certification",
            "Project management",
            "Quality standards"
        ],
        "Entry Level": [
            "Engineer"
        ],
        "Growth": [
            "Senior Engineer",
            "Technical Director"
        ]
    },

    "Merchant Navy Officer": {
        "Foundation": [
            "Marine studies basics",
            "Navigation",
            "Physical fitness"
        ],
        "Skill Building": [
            "Sea training",
            "Ship operations",
            "Safety protocols"
        ],
        "Entry Level": [
            "Deck Officer"
        ],
        "Growth": [
            "Captain",
            "Marine Superintendent"
        ]
    },

    # ================================
    # Skilled & Emerging Careers (4)
    # ================================
    "Digital Marketing Specialist": {
        "Foundation": [
            "Marketing basics",
            "Digital platforms",
            "Content fundamentals"
        ],
        "Skill Building": [
            "SEO/SEM",
            "Social media ads",
            "Analytics tools"
        ],
        "Entry Level": [
            "Digital Marketer"
        ],
        "Growth": [
            "Marketing Strategist",
            "Growth Head"
        ]
    },

    "SEO / Growth Analyst": {
        "Foundation": [
            "Search engine basics",
            "Web analytics",
            "Data interpretation"
        ],
        "Skill Building": [
            "SEO tools",
            "Conversion optimization",
            "A/B testing"
        ],
        "Entry Level": [
            "SEO Analyst"
        ],
        "Growth": [
            "Growth Manager",
            "Digital Consultant"
        ]
    },

    "Technical Content Creator": {
        "Foundation": [
            "Technical understanding",
            "Writing skills",
            "Audience awareness"
        ],
        "Skill Building": [
            "Blogging",
            "Video creation",
            "SEO writing"
        ],
        "Entry Level": [
            "Technical Writer"
        ],
        "Growth": [
            "Content Lead",
            "Independent Creator"
        ]
    },

    "No-Code / Automation Specialist": {
        "Foundation": [
            "Workflow understanding",
            "Basic logic",
            "Automation concepts"
        ],
        "Skill Building": [
            "No-code tools",
            "API integration",
            "Process automation"
        ],
        "Entry Level": [
            "Automation Specialist"
        ],
        "Growth": [
            "Automation Architect",
            "Consultant"
        ]
    }
}

# =====================================================
# SESSION STATE & STYLING
# =====================================================
if "page" not in st.session_state: st.session_state.page = "questionnaire"
if "profile" not in st.session_state: st.session_state.profile = {}
if "selected_career_name" not in st.session_state: st.session_state.selected_career_name = None
if "show_results_btn" not in st.session_state: st.session_state.show_results_btn = False
if "show_roadmap_btn" not in st.session_state: st.session_state.show_roadmap_btn = False

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .career-card { background-color: white; padding: 1.5rem; border-radius: 18px; box-shadow: 0px 4px 20px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; margin-bottom: 20px;}
    .fit-badge { color: white; padding: 5px 12px; border-radius: 50px; font-weight: 700; font-size: 0.85rem; }
    .career-title { font-size: 1.4rem; font-weight: 800; color: #0F172A; margin: 10px 0; }
    .stButton > button { width: 100%; border-radius: 10px; font-weight: 600; padding: 0.6rem;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## 🧭 PathWise")
    st.divider()
    if st.button("🏠 Questionnaire"):
        st.session_state.page = "questionnaire"
        st.rerun()
    if st.session_state.show_results_btn:
        if st.button("🎯 My Results"):
            st.session_state.page = "results"
            st.rerun()
    if st.session_state.show_roadmap_btn:
        if st.button("🗺️ Career Roadmap"):
            st.session_state.page = "roadmap"
            st.rerun()

# =====================================================
# PAGES
# =====================================================
def questionnaire_page():
    st.title("Build Your Profile")
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        edu = c1.selectbox("Education", ["Postgraduate", "Undergraduate", "School (Classes 9-12)", "Other"])
        field = c2.selectbox("Field", ["Engineering", "Science", "Commerce", "Management", "Arts and Humanities", "Other"])
        
        st.divider()
        st.subheader("Mindset & Stability")
        c3, c4, c5 = st.columns(3)
        rate = c3.radio("Learning Pace", ["Slow", "Average", "Fast"])
        risk = c4.radio("Risk Tolerance", ["Low Risk", "Moderate Risk", "High Risk"])
        time_h = c5.radio("Time to Stability", ["Immediate (0-1 year)", "Mid Term (1-3 years)", "Long Term (3+ years)"])
        
        st.divider()
        st.subheader("Interests & Strengths")
        ints = st.multiselect("Interests (Pick 3)", mlb_int.classes_.tolist(), max_selections=3)
        strs = st.multiselect("Strengths (Pick 3)", mlb_str.classes_.tolist(), max_selections=3)
        
        if st.form_submit_button("Predict Careers →"):
            st.session_state.profile = {"education": edu, "field": field, "interests": ints, "strengths": strs, "learning_rate": rate, "time_horizon": time_h, "risk": risk}
            st.session_state.show_results_btn = True
            st.session_state.page = "results"
            st.rerun()

def results_page():
    st.title("Your AI Matches")
    matches = get_ml_recommendations(st.session_state.profile)
    cols = st.columns(3)
    for i, match in enumerate(matches):
        with cols[i]:
            score = match['fit_score']
            color = "#0D9488" if score >= 90 else "#14B8A6"
            st.markdown(f"""
            <div class="career-card">
                <span class="fit-badge" style="background-color: {color};">{score}% Match</span>
                <div class="career-title">{match['career_name']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View Roadmap →", key=f"b_{i}"):
                st.session_state.selected_career_name = match['career_name']
                st.session_state.show_roadmap_btn = True
                st.session_state.page = "roadmap"
                st.rerun()

def roadmap_page():
    name = st.session_state.selected_career_name
    st.title(f"Roadmap: {name}")
    roadmap = CAREER_ROADMAPS.get(name)
    if roadmap:
        for phase, steps in roadmap.items():
            st.markdown(f"### 🔹 {phase}")
            for s in steps: st.markdown(f"- {s}")
            st.divider()
    if st.button("← Back"):
        st.session_state.page = "results"
        st.rerun()

# =====================================================
# ROUTER
# =====================================================
if st.session_state.page == "questionnaire": questionnaire_page()
elif st.session_state.page == "results": results_page()
elif st.session_state.page == "roadmap": roadmap_page()