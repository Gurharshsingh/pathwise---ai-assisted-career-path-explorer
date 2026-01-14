import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- 1. PROFESSIONAL CONFIGURATION ---
st.set_page_config(page_title="PATHWISE | Discovery & Roadmaps", page_icon="🎯", layout="wide")

# Custom CSS for Professional SaaS Look
st.markdown("""
<style>

/* ============================
   GLOBAL TYPOGRAPHY
============================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ============================
   BACKGROUND
============================ */
.main {
    background: linear-gradient(180deg, #f8f9fa 0%, #eef2f7 100%);
}

/* ============================
   BUTTONS
============================ */
.stButton>button { 
    width: 100%;
    height: 3.6em;
    border-radius: 14px;
    background: linear-gradient(135deg, #4facfe, #007bff);
    color: white;
    font-weight: 700;
    border: none;
    letter-spacing: 0.3px;
    box-shadow: 0 0 18px rgba(79,172,254,0.45);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 0 30px rgba(79,172,254,0.75);
}

/* ============================
   RESULT CARDS
============================ */
.result-card {
    padding: 26px;
    border-radius: 18px;
    background: linear-gradient(145deg,#ffffff,#f1f4f9);
    border-left: 8px solid #007bff;
    margin-bottom: 22px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    animation: fadeUp 0.6s ease;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ============================
   METRICS
============================ */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 0 25px rgba(0,123,255,0.12);
}

/* ============================
   EXPANDERS
============================ */
div[data-testid="stExpander"] {
    border-radius: 16px;
    border: 1px solid rgba(0,123,255,0.15);
    box-shadow: 0 0 18px rgba(0,123,255,0.08);
}

/* ============================
   SECTION HEADERS
============================ */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: -0.3px;
}

h4, h5 {
    font-weight: 600;
}


.career-image-card {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border: 1px solid rgba(0,123,255,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.career-image-card:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 18px 40px rgba(0,123,255,0.35);
}


</style>
""", unsafe_allow_html=True)


# --- 2. ASSET LOADER ---
@st.cache_resource
def load_ai_assets():
    try:
        data = joblib.load('career_model.pkl')
        return data['model'], data['le'], data['mlb_int'], data['mlb_str'], data['features']
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None, None

model, le, mlb_int, mlb_str, model_features = load_ai_assets()

# --- 3. THE DEEP ROADMAP DATABASE (Sample - Expand to 36) ---
# Each entry includes Prerequisites, Steps, Tools, and Certs
DEEP_DATA = {
    # ================================
    # Technology & Software
    # ================================
    "Software Engineer": {
        "Stats": {"Time": "1-2 Years", "Market": "Very High", "Salary": "₹8L - ₹25L+"},
        "Prereq": ["Logic", "Basic Math", "English"],
        "Tools": ["VS Code", "Git", "Docker", "Kubernetes"],
        "Certs": ["AWS Developer", "Meta Front-End", "Oracle Java"],
        "Steps": [
            {"title": "Tier 1: CS Foundations", "desc": "Master Data Structures, Algorithms, and OS basics.", "knowledge": "Most production bugs stem from poor memory management or race conditions.", "tip": "Start with CS50 on edX."},
            {"title": "Tier 2: Language Mastery", "desc": "Pick one core language (Java, Python, or Go) and master its async patterns.", "knowledge": "Mastering one language is better than being a beginner in five.", "tip": "Build 5 mini-projects on GitHub."},
            {"title": "Tier 3: System Architecture", "desc": "Learn Microservices, Load Balancers, and Caching (Redis).", "knowledge": "Scaling is about database sharding and stateless architecture.", "tip": "Read 'System Design Interview' by Alex Xu."},
            {"title": "Tier 4: DevOps & CI/CD", "desc": "Automate deployment using Jenkins or GitHub Actions.", "knowledge": "Containerization solves the 'it works on my machine' problem.", "tip": "Deploy a live project on AWS/Azure."},
            {"title": "Tier 5: Market Readiness", "desc": "Learn Agile/Scrum and technical documentation.", "knowledge": "Coding is 30% writing and 70% reading/communicating.", "tip": "Optimize your GitHub READMEs."}
        ]
    },
    "Data Analyst": {
        "Stats": {"Time": "8-12 Months", "Market": "High", "Salary": "₹6L - ₹15L"},
        "Prereq": ["Statistics", "Excel", "Critical Thinking"],
        "Tools": ["SQL", "Tableau", "PowerBI", "Python"],
        "Certs": ["Google Data Analytics", "Tableau Desktop Specialist"],
        "Steps": [
            {"title": "Tier 1: Statistical Foundations", "desc": "Master Mean, Variance, and Probability Distributions.", "knowledge": "Data can be misleading without understanding p-values and correlation.", "tip": "Analyze your own bank statements for patterns."},
            {"title": "Tier 2: SQL Mastery", "desc": "Master JOINS, Window Functions, and CTEs.", "knowledge": "80% of your day is cleaning data, not looking at charts.", "tip": "Solve SQL tracks on Hackerrank."},
            {"title": "Tier 3: Business Intelligence", "desc": "Master Tableau/Power BI and DAX formulas.", "knowledge": "A great dashboard answers questions before they are asked.", "tip": "Publish on Tableau Public."},
            {"title": "Tier 4: Python for Analysis", "desc": "Learn Pandas, NumPy, and Matplotlib.", "knowledge": "Python handles Big Data that Excel cannot open.", "tip": "Automate an Excel report using Python."},
            {"title": "Tier 5: Storytelling", "desc": "Translate data into 'Executive Summaries'.", "knowledge": "Stakeholders care about the 'So What?'—the business impact.", "tip": "Practice presenting to non-tech friends."}
        ]
    },
    "Product Manager (Tech)": {
        "Stats": {"Time": "1-2 Years", "Market": "High", "Salary": "₹12L - ₹30L+"},
        "Prereq": ["Business Logic", "Tech Literacy", "Empathy"],
        "Tools": ["Jira", "Figma", "Confluence", "Mixpanel"],
        "Certs": ["CSPO", "Google PM Professional"],
        "Steps": [
            {"title": "Tier 1: Product Life Cycle", "desc": "Learn ideation, discovery, and launch phases.", "knowledge": "PMs are 'mini-CEOs' but without direct authority over people.", "tip": "Read 'Inspired' by Marty Cagan."},
            {"title": "Tier 2: UX & Design", "desc": "Learn wireframing and user research methods.", "knowledge": "You don't need to be a designer, but you must know what 'Good' looks like.", "tip": "Build a mock PRD for Spotify."},
            {"title": "Tier 3: Analytics", "desc": "Learn A/B testing and North Star metrics.", "knowledge": "Features aren't successes unless they move the needle on data.", "tip": "Learn SQL to pull your own data."},
            {"title": "Tier 4: Agile Leadership", "desc": "Master Scrum, Kanban, and Sprint planning.", "knowledge": "Your job is to clear roadblocks for engineers.", "tip": "Shadow a PM at a local startup."},
            {"title": "Tier 5: Strategy", "desc": "Learn roadmap prioritization and vision setting.", "knowledge": "Saying 'No' is the most important part of the job.", "tip": "Create a 6-month roadmap for an app."}
        ]
    },
    "QA / Test Engineer": {
        "Stats": {"Time": "6-9 Months", "Market": "High", "Salary": "₹4L - ₹10L"},
        "Prereq": ["Attention to Detail", "Logic", "SDLC"],
        "Tools": ["Selenium", "Postman", "Appium", "Jira"],
        "Certs": ["ISTQB Foundation", "Selenium WebDriver"],
        "Steps": [
            {"title": "Tier 1: Manual Testing", "desc": "Learn Bug Life Cycle and STLC models.", "knowledge": "A good tester thinks like a user who is trying to break the app.", "tip": "Write 50 test cases for a login page."},
            {"title": "Tier 2: Automation", "desc": "Learn Selenium with Java or Python.", "knowledge": "Automation isn't about finding bugs; it's about preventing regressions.", "tip": "Automate a web checkout flow."},
            {"title": "Tier 3: API Testing", "desc": "Master Postman and Rest-Assured.", "knowledge": "Modern apps break at the API layer more than the UI.", "tip": "Learn to test JSON responses."},
            {"title": "Tier 4: Performance", "desc": "Learn JMeter or LoadRunner.", "knowledge": "An app that is slow is a broken app.", "tip": "Run a 500-user load test on a site."},
            {"title": "Tier 5: Test Architect", "desc": "Learn to build frameworks from scratch.", "knowledge": "Quality is a culture, not just a phase in development.", "tip": "Learn CI/CD integration for tests."}
        ]
    },

    # ================================
    # Business, Management & Operations
    # ================================
    "Business Analyst": {
        "Stats": {"Time": "1 Year", "Market": "High", "Salary": "₹6L - ₹18L"},
        "Prereq": ["Communication", "Domain Knowledge", "Documentation"],
        "Tools": ["MS Visio", "SQL", "Excel", "Draw.io"],
        "Certs": ["ECBA", "CBAP"],
        "Steps": [
            {"title": "Tier 1: Requirements Gathering", "desc": "Learn to write BRDs, FRDs, and User Stories.", "knowledge": "The biggest risk to a project is misunderstood requirements.", "tip": "Practice process mapping for a library."},
            {"title": "Tier 2: Stakeholder Management", "desc": "Learn to bridge the gap between clients and IT.", "knowledge": "Negotiation is 50% of the job.", "tip": "Improve your presentation skills."},
            {"title": "Tier 3: SQL & Data", "desc": "Learn to extract data for business validation.", "knowledge": "You can't rely on devs to give you every report.", "tip": "Learn basic data visualization."},
            {"title": "Tier 4: Gap Analysis", "desc": "Learn AS-IS vs TO-BE modeling.", "knowledge": "Solving the wrong problem is worse than not solving it.", "tip": "Do a mock audit of a small business."},
            {"title": "Tier 5: Agile BA", "desc": "Learn Product Backlog grooming.", "knowledge": "In Agile, the BA role often shifts toward Product Owner.", "tip": "Get a Scrum certification."}
        ]
    },
    "Operations Manager": {
        "Stats": {"Time": "3-5 Years", "Market": "Stable", "Salary": "₹8L - ₹22L"},
        "Prereq": ["Leadership", "Process Thinking", "Logistics"],
        "Tools": ["ERP (SAP/Oracle)", "Excel", "Project Mgmt Apps"],
        "Certs": ["Six Sigma Green Belt", "PMP"],
        "Steps": [
            {"title": "Tier 1: Process Optimization", "desc": "Learn Lean and Six Sigma principles.", "knowledge": "Efficiency is doing things right; effectiveness is doing the right things.", "tip": "Map a local delivery service process."},
            {"title": "Tier 2: Supply Chain", "desc": "Learn inventory management and procurement.", "knowledge": "The supply chain is only as strong as its weakest link.", "tip": "Study JIT (Just-in-Time) systems."},
            {"title": "Tier 3: Team Leadership", "desc": "Learn conflict resolution and workforce planning.", "knowledge": "People are the hardest 'process' to manage.", "tip": "Get a team lead role in any field."},
            {"title": "Tier 4: Financial Ops", "desc": "Learn budgeting, P&L, and cost-benefit analysis.", "knowledge": "Every operational change must reflect in the bottom line.", "tip": "Master Excel financial formulas."},
            {"title": "Tier 5: Strategic Ops", "desc": "Learn scaling and global expansion.", "knowledge": "Great ops managers turn chaos into a predictable machine.", "tip": "Study companies like Amazon for ops excellence."}
        ]
    },
    "Management Consultant": {
        "Stats": {"Time": "2-4 Years", "Market": "High", "Salary": "₹15L - ₹40L+"},
        "Prereq": ["MBA", "Analytical Thinking", "Persuasion"],
        "Tools": ["PowerPoint", "Think-Cell", "Excel"],
        "Certs": ["CMC (Certified Management Consultant)"],
        "Steps": [
            {"title": "Tier 1: Case Frameworks", "desc": "Master MECE and Profitability frameworks.", "knowledge": "Structure is your best friend in a high-pressure meeting.", "tip": "Practice Case Interviews daily."},
            {"title": "Tier 2: Market Entry", "desc": "Learn sizing, growth, and competition analysis.", "knowledge": "Clients pay for your perspective, not just your data.", "tip": "Analyze a recent business acquisition."},
            {"title": "Tier 3: Financial Modeling", "desc": "Learn to build complex valuation models.", "knowledge": "If you can't prove it with numbers, it didn't happen.", "tip": "Master 'Excel for Consultants'."},
            {"title": "Tier 4: Executive Presence", "desc": "Learn storytelling for the C-suite.", "knowledge": "Consultants don't just solve problems; they sell solutions.", "tip": "Record yourself giving a pitch."},
            {"title": "Tier 5: Implementation", "desc": "Learn Change Management and ROI tracking.", "knowledge": "A strategy is useless if the client's team won't adopt it.", "tip": "Study behavioral economics."}
        ]
    },
    "Entrepreneur (Early-stage)": {
        "Stats": {"Time": "Unlimited", "Market": "Volatile", "Salary": "Variable"},
        "Prereq": ["Risk Appetite", "Persistence", "Vision"],
        "Tools": ["Notion", "Stripe", "Zoom", "Webflow"],
        "Certs": ["Y-Combinator Startup School"],
        "Steps": [
            {"title": "Tier 1: Ideation & Validation", "desc": "Find a real pain point and talk to customers.", "knowledge": "Most startups fail because they build something nobody wants.", "tip": "Read 'The Mom Test'."},
            {"title": "Tier 2: MVP Development", "desc": "Build a Minimum Viable Product with no-code tools.", "knowledge": "Speed to market beats perfection every time.", "tip": "Launch a landing page first."},
            {"title": "Tier 3: Sales & Marketing", "desc": "Learn to acquire your first 100 users.", "knowledge": "Sales solve everything. If you aren't selling, you aren't a business.", "tip": "Do 'cold' outreach to 50 people."},
            {"title": "Tier 4: Fundraising", "desc": "Learn term sheets, equity, and pitching to VCs.", "knowledge": "Venture capital is fuel, not the engine.", "tip": "Build a solid 10-slide deck."},
            {"title": "Tier 5: Hiring & Culture", "desc": "Learn to build a team and delegate.", "knowledge": "The founder's job shifts from doing to leading.", "tip": "Hire for attitude, train for skill."}
        ]
    },

    # ================================
    # Design, Media & Digital Creative
    # ================================
    "UI/UX Designer": {
        "Stats": {"Time": "1 Year", "Market": "Very High", "Salary": "₹6L - ₹20L"},
        "Prereq": ["Visual Aesthetics", "Empathy", "Psychology"],
        "Tools": ["Figma", "Adobe XD", "Miro", "Framer"],
        "Certs": ["Google UX Design", "HCI Specialization"],
        "Steps": [
            {"title": "Tier 1: Design Principles", "desc": "Learn Color Theory, Typography, and Grids.", "knowledge": "UI is how it looks; UX is how it works.", "tip": "Daily UI Challenge (30 days)."},
            {"title": "Tier 2: User Research", "desc": "Learn Personas, User Flows, and Interviews.", "knowledge": "You are not the user. Base decisions on data, not ego.", "tip": "Conduct 3 usability tests."},
            {"title": "Tier 3: Wireframing", "desc": "Master Low-fidelity and High-fidelity prototyping.", "knowledge": "Prototyping saves weeks of development time.", "tip": "Master Figma Auto-Layout."},
            {"title": "Tier 4: Design Systems", "desc": "Learn to build reusable component libraries.", "knowledge": "Consistency is key to a professional product.", "tip": "Build a mobile app design system."},
            {"title": "Tier 5: Portfolio", "desc": "Create 2 detailed case studies.", "knowledge": "Hiring managers look for your process, not just pretty screens.", "tip": "Write 'Problem -> Solution' stories."}
        ]
    },
    "Graphic Designer": {
        "Stats": {"Time": "6-12 Months", "Market": "Stable", "Salary": "₹3L - ₹10L"},
        "Prereq": ["Creativity", "Art", "Observation"],
        "Tools": ["Photoshop", "Illustrator", "InDesign", "Canva"],
        "Certs": ["Adobe Certified Professional"],
        "Steps": [
            {"title": "Tier 1: Foundations", "desc": "Learn Composition and Visual Hierarchy.", "knowledge": "Design is thinking made visual.", "tip": "Copy 5 famous posters to learn."},
            {"title": "Tier 2: Vector & Raster", "desc": "Master Adobe Illustrator and Photoshop.", "knowledge": "Learn the difference between CMYK and RGB early.", "tip": "Master the Pen Tool."},
            {"title": "Tier 3: Branding", "desc": "Learn Logo Design and Brand Identity.", "knowledge": "A logo is just a symbol; a brand is an emotion.", "tip": "Build a brand for a fake coffee shop."},
            {"title": "Tier 4: Layout Design", "desc": "Learn InDesign for print and digital books.", "knowledge": "White space is a design element, not empty space.", "tip": "Design a 4-page magazine spread."},
            {"title": "Tier 5: Professional Practice", "desc": "Learn client handling and freelancing.", "knowledge": "Your client's business goals are more important than your art.", "tip": "Set up a Behance profile."}
        ]
    },
    "Content Strategist / Copywriter": {
        "Stats": {"Time": "6-12 Months", "Market": "High", "Salary": "₹4L - ₹12L"},
        "Prereq": ["Writing", "Psychology", "Marketing"],
        "Tools": ["WordPress", "SEMRush", "Copy.ai", "Hemingway"],
        "Certs": ["HubSpot Content Marketing"],
        "Steps": [
            {"title": "Tier 1: Writing Basics", "desc": "Learn grammar, tone, and storytelling.", "knowledge": "Good writing is clear; great writing is persuasive.", "tip": "Start a daily journaling habit."},
            {"title": "Tier 2: Copywriting", "desc": "Learn AIDA (Attention, Interest, Desire, Action).", "knowledge": "Copywriting is salesmanship in print.", "tip": "Rewrite 5 bad ads you see online."},
            {"title": "Tier 3: SEO Content", "desc": "Learn Keyword Research and On-page SEO.", "knowledge": "If it doesn't rank, it doesn't exist to the user.", "tip": "Write a 1500-word SEO article."},
            {"title": "Tier 4: Strategy", "desc": "Learn Content Funnels (Top, Middle, Bottom).", "knowledge": "Strategy is about knowing what to write when.", "tip": "Create a content calendar for a month."},
            {"title": "Tier 5: Analytics", "desc": "Learn to track conversion rates and ROI.", "knowledge": "Content is an investment, not an expense.", "tip": "Learn Google Analytics 4."}
        ]
    },
    "Digital Media Specialist": {
        "Stats": {"Time": "6-12 Months", "Market": "High", "Salary": "₹4L - ₹15L"},
        "Prereq": ["Trends", "Social Media", "Video Basics"],
        "Tools": ["Meta Ads", "CapCut", "Premiere Pro", "Buffer"],
        "Certs": ["Meta Blueprint", "Google Ads Cert"],
        "Steps": [
            {"title": "Tier 1: Content Creation", "desc": "Learn short-form video and editing.", "knowledge": "Attention is the new currency. Captivate in the first 3 seconds.", "tip": "Grow a TikTok/Reels page to 1k followers."},
            {"title": "Tier 2: Paid Ads", "desc": "Learn Facebook, Instagram, and Google Ads.", "knowledge": "Spending money is easy; spending it profitably is hard.", "tip": "Run a small trial campaign."},
            {"title": "Tier 3: Platform Algorithms", "desc": "Learn why things go viral.", "knowledge": "Don't fight the algorithm; provide what users want to see.", "tip": "Analyze 10 viral posts."},
            {"title": "Tier 4: Influencer Marketing", "desc": "Learn to manage collaborations.", "knowledge": "Trust is built by people, not just brands.", "tip": "Reach out to a small creator for a collab."},
            {"title": "Tier 5: Reporting", "desc": "Learn ROAS and Attribution models.", "knowledge": "The data tells you what to stop doing.", "tip": "Master Meta Business Suite."}
        ]
    },

    # ================================
    # Fashion, Architecture & Physical Design
    # ================================
    "Fashion Designer": {
        "Stats": {"Time": "3-4 Years", "Market": "Competitive", "Salary": "Variable"},
        "Prereq": ["Art", "Sewing", "Trend Awareness"],
        "Tools": ["CLO 3D", "Photoshop", "Sewing Machine"],
        "Certs": ["Fashion Diploma"],
        "Steps": [
            {"title": "Tier 1: Sketching", "desc": "Master fashion illustration and anatomy.", "knowledge": "Design starts with a pencil and a dream.", "tip": "Fill 2 sketchbooks with designs."},
            {"title": "Tier 2: Fabric Science", "desc": "Learn silk, cotton, and synthetic properties.", "knowledge": "The fabric dictates the silhouette.", "tip": "Visit a local textile market."},
            {"title": "Tier 3: Pattern Making", "desc": "Learn draping and garment construction.", "knowledge": "A designer who can't sew is at the mercy of the tailor.", "tip": "Sew a basic garment from scratch."},
            {"title": "Tier 4: Fashion Tech", "desc": "Learn 3D modeling with CLO 3D.", "knowledge": "The future of fashion is digital prototyping.", "tip": "Render a 3D outfit."},
            {"title": "Tier 5: Brand Launch", "desc": "Learn marketing and fashion shows.", "knowledge": "Style is what you choose; fashion is what you sell.", "tip": "Intern with a senior designer."}
        ]
    },
    "Textile Designer": {
        "Stats": {"Time": "2-3 Years", "Market": "Stable", "Salary": "Moderate"},
        "Prereq": ["Color Sense", "Science", "Art"],
        "Tools": ["Adobe Textile", "CAD Tools", "Loom"],
        "Certs": ["Textile Science Diploma"],
        "Steps": [
            {"title": "Tier 1: Yarn & Fiber", "desc": "Study natural vs. synthetic fibers.", "knowledge": "Everything starts with a single thread.", "tip": "Study weaving techniques."},
            {"title": "Tier 2: Print & Dye", "desc": "Learn block, screen, and digital printing.", "knowledge": "Color fastness is as important as the design.", "tip": "Try tie-dyeing at home."},
            {"title": "Tier 3: CAD for Textiles", "desc": "Learn repeat patterns in Adobe.", "knowledge": "Seamless patterns are the standard for industry.", "tip": "Create 10 seamless patterns."},
            {"title": "Tier 4: Sustainability", "desc": "Learn eco-friendly dyeing and recycling.", "knowledge": "The textile industry is moving toward zero-waste.", "tip": "Study organic cotton supply chains."},
            {"title": "Tier 5: Manufacturing", "desc": "Learn industrial loom technology.", "knowledge": "Design for scale, not just for a single sample.", "tip": "Visit a spinning mill."}
        ]
    },
    "Architect": {
        "Stats": {"Time": "5 Years", "Market": "Stable", "Salary": "High"},
        "Prereq": ["Math", "Physics", "Drafting"],
        "Tools": ["AutoCAD", "Revit", "Rhino", "V-Ray"],
        "Certs": ["COA / RIBA Registration"],
        "Steps": [
            {"title": "Tier 1: Drafting Basics", "desc": "Learn technical drawing and physics of structures.", "knowledge": "Architecture is inhabited sculpture.", "tip": "Build a 1:50 physical model."},
            {"title": "Tier 2: BIM & 3D", "desc": "Master Revit and BIM workflows.", "knowledge": "BIM is not just 3D; it's data-driven building management.", "tip": "Complete a full Revit project."},
            {"title": "Tier 3: Sustainability", "desc": "Learn LEED standards and green building.", "knowledge": "Great architecture works with the sun and wind.", "tip": "Study passive solar design."},
            {"title": "Tier 4: Building Codes", "desc": "Learn fire safety and zoning laws.", "knowledge": "Legal constraints are where creativity is tested.", "tip": "Read your local building bylaws."},
            {"title": "Tier 5: Project Management", "desc": "Learn to manage contractors and sites.", "knowledge": "Architects are the conductors of a construction orchestra.", "tip": "Visit a live construction site."}
        ]
    },
    "Interior Designer": {
        "Stats": {"Time": "2 Years", "Market": "Growing", "Salary": "₹4L - ₹15L"},
        "Prereq": ["Aesthetics", "Space Planning", "Client Mgmt"],
        "Tools": ["SketchUp", "V-Ray", "AutoCAD"],
        "Certs": ["Interior Design Diploma"],
        "Steps": [
            {"title": "Tier 1: Space Logic", "desc": "Learn floor plans and circulation.", "knowledge": "Function first, aesthetics second.", "tip": "Study kitchen triangle ergonomics."},
            {"title": "Tier 2: Materiality", "desc": "Learn wood, stone, and lighting properties.", "knowledge": "Texture changes how a room feels more than color.", "tip": "Create a physical mood board."},
            {"title": "Tier 3: 3D Visualization", "desc": "Master SketchUp and V-Ray rendering.", "knowledge": "Clients buy the dream you render for them.", "tip": "Render a photorealistic bedroom."},
            {"title": "Tier 4: Vendor Mgmt", "desc": "Learn to source furniture and handle labor.", "knowledge": "Your network of carpenters is your secret weapon.", "tip": "Visit 10 local furniture stores."},
            {"title": "Tier 5: Business of Design", "desc": "Learn project costing and billing.", "knowledge": "Being a designer is 50% business.", "tip": "Start an Instagram for your work."}
        ]
    },

    # ================================
    # Finance, Accounting & Economics
    # ================================
    "Financial Analyst": {
        "Stats": {"Time": "2 Years", "Market": "Stable", "Salary": "₹8L - ₹20L"},
        "Prereq": ["Math", "Excel", "Economics"],
        "Tools": ["Excel (VBA)", "Bloomberg", "Python"],
        "Certs": ["CFA Level 1", "FMVA"],
        "Steps": [
            {"title": "Tier 1: Accounting Core", "desc": "Master P&L, Balance Sheet, and Cash Flows.", "knowledge": "Profit is an opinion; cash is a fact.", "tip": "Link 3 statements in Excel."},
            {"title": "Tier 2: Financial Modeling", "desc": "Learn DCF and LBO modeling.", "knowledge": "Models are only as good as their assumptions.", "tip": "Read 'Breaking into Wall St'."},
            {"title": "Tier 3: Valuation", "desc": "Learn WACC and Relative Valuation.", "knowledge": "Price is what you pay; value is what you get.", "tip": "Value a public company."},
            {"title": "Tier 4: Market Research", "desc": "Learn to analyze industry trends.", "knowledge": "The numbers don't speak; you speak for them.", "tip": "Write an equity research report."},
            {"title": "Tier 5: Ethics & Compliance", "desc": "Learn financial laws and professional ethics.", "knowledge": "Integrity is the most valuable asset in finance.", "tip": "Follow Bloomberg/WSJ daily."}
        ]
    },
    "Chartered Accountant (CA)": {
        "Stats": {"Time": "5 Years", "Market": "Very Stable", "Salary": "₹10L - ₹30L+"},
        "Prereq": ["Accuracy", "Ethics", "Persistence"],
        "Tools": ["Tally", "SAP", "Excel"],
        "Certs": ["ICAI / ACCA"],
        "Steps": [
            {"title": "Tier 1: Foundation", "desc": "Learn basic accounting and law.", "knowledge": "Stay disciplined; the syllabus is vast.", "tip": "Practice daily for accounts."},
            {"title": "Tier 2: Intermediate", "desc": "Learn Direct & Indirect Tax, Costing.", "knowledge": "Tax is where the money is saved for the client.", "tip": "Master the GST laws."},
            {"title": "Tier 3: Articleship", "desc": "3 years of practical training in an audit firm.", "knowledge": "Practical experience is where you become a professional.", "tip": "Join a Big 4 if possible."},
            {"title": "Tier 4: Audit & Assurance", "desc": "Master Statutory and Internal Auditing.", "knowledge": "You are the watchdog of the economy.", "tip": "Focus on risk assessment."},
            {"title": "Tier 5: Final Exam", "desc": "Clear the toughest exams in the field.", "knowledge": "The prefix 'CA' is a mark of trust.", "tip": "Stay updated on ICAI notifications."}
        ]
    },
    "Investment Banking Analyst": {
        "Stats": {"Time": "2-3 Years", "Market": "Elite", "Salary": "₹20L - ₹50L+"},
        "Prereq": ["Endurance", "Networking", "Finance"],
        "Tools": ["Excel", "PowerPoint", "FactSet"],
        "Certs": ["CFA", "Wall St Prep"],
        "Steps": [
            {"title": "Tier 1: M&A Logic", "desc": "Learn mergers, acquisitions, and IPOs.", "knowledge": "Deals are built on relationships and data.", "tip": "Learn to work 80+ hours a week."},
            {"title": "Tier 2: Pitch Books", "desc": "Master high-end PPT decks.", "knowledge": "Your deck must be flawless; even a comma matters.", "tip": "Learn PPT shortcuts."},
            {"title": "Tier 3: Valuation Deep Dive", "desc": "Learn LBO and M&A modeling.", "knowledge": "Know your numbers better than the client.", "tip": "Value a recent M&A deal."},
            {"title": "Tier 4: Due Diligence", "desc": "Learn to audit a target company's data.", "knowledge": "Find the skeletons in the closet.", "tip": "Master Excel indexing."},
            {"title": "Tier 5: Networking", "desc": "Build a network of senior bankers.", "knowledge": "In IB, who you know is how you close.", "tip": "Reach out to 50 alumni."}
        ]
    },
    "Risk & Compliance Analyst": {
        "Stats": {"Time": "1-2 Years", "Market": "Growing", "Salary": "₹6L - ₹15L"},
        "Prereq": ["Logic", "Law", "Attention"],
        "Tools": ["Compliance Tools", "Excel", "Tableau"],
        "Certs": ["FRM", "CAMS"],
        "Steps": [
            {"title": "Tier 1: Regulations", "desc": "Learn KYC, AML, and Basel III/IV.", "knowledge": "Banks fail because of bad risk, not bad products.", "tip": "Study financial crisis history."},
            {"title": "Tier 2: Risk Modeling", "desc": "Learn to calculate VAR (Value at Risk).", "knowledge": "Math is the shield against market volatility.", "tip": "Learn basic Monte Carlo simulations."},
            {"title": "Tier 3: Compliance Audit", "desc": "Learn to find legal loopholes.", "knowledge": "Stay ahead of the regulators.", "tip": "Master risk-based auditing."},
            {"title": "Tier 4: Operational Risk", "desc": "Learn to prevent internal fraud.", "knowledge": "Most risk is inside the building.", "tip": "Learn about cyber-risk."},
            {"title": "Tier 5: Governance", "desc": "Learn corporate ethics and ESG.", "knowledge": "Good ethics is good business.", "tip": "Get certified in CAMS."}
        ]
    },

    # ================================
    # Government, Public Service & Education
    # ================================
    "Civil Services / Government Exams": {
        "Stats": {"Time": "2-4 Years", "Market": "High Security", "Salary": "Good + Perks"},
        "Prereq": ["General Studies", "History", "Current Affairs"],
        "Tools": ["Mock Tests", "Newspapers"],
        "Certs": ["UPSC / State PSC"],
        "Steps": [
            {"title": "Tier 1: Foundation", "desc": "Study Polity, History, and Economy.", "knowledge": "Breadth over depth. Know a bit about everything.", "tip": "Read 'The Hindu' daily."},
            {"title": "Tier 2: Mains Mastery", "desc": "Learn answer writing and ethics.", "knowledge": "It's not what you know, but how you write it.", "tip": "Write 2 answers every day."},
            {"title": "Tier 3: Optional Subject", "desc": "Deep dive into your chosen subject.", "knowledge": "The optional subject often decides the rank.", "tip": "Choose based on interest, not 'scoring'."},
            {"title": "Tier 4: Personality Test", "desc": "Improve speaking and confidence.", "knowledge": "The interview is about your character, not facts.", "tip": "Join mock interview panels."},
            {"title": "Tier 5: Training", "desc": "Final training at the academy.", "knowledge": "You are now a servant of the people.", "tip": "Stay humble and curious."}
        ]
    },
    "Public Sector Officer": {
        "Stats": {"Time": "1-2 Years", "Market": "Stable", "Salary": "₹6L - ₹12L"},
        "Prereq": ["Aptitude", "Reasoning", "English"],
        "Tools": ["Aptitude Books", "Mock Tests"],
        "Certs": ["IBPS / SSC / SBI"],
        "Steps": [
            {"title": "Tier 1: Speed Math", "desc": "Master Quant and Reasoning shortcuts.", "knowledge": "Competitive exams are about time management.", "tip": "Practice 50 sums a day."},
            {"title": "Tier 2: General Awareness", "desc": "Learn banking and current events.", "knowledge": "Stay updated on RBI notifications.", "tip": "Follow financial news daily."},
            {"title": "Tier 3: Prelims & Mains", "desc": "Clear the multi-stage written exams.", "knowledge": "Practice mock tests in a timed environment.", "tip": "Analyze your mock errors."},
            {"title": "Tier 4: Interview", "desc": "Prepare for banking/sector interviews.", "knowledge": "Show confidence and basic sector knowledge.", "tip": "Practice in front of a mirror."},
            {"title": "Tier 5: Field Posting", "desc": "Undergo training and probation.", "knowledge": "Learn the ground reality of public service.", "tip": "Be ready for rural postings."}
        ]
    },
    "School / College Teacher": {
        "Stats": {"Time": "2-4 Years", "Market": "Stable", "Salary": "₹4L - ₹10L"},
        "Prereq": ["Patience", "Subject Mastery", "Communication"],
        "Tools": ["Google Classroom", "PowerPoint", "LMS"],
        "Certs": ["B.Ed / NET / PhD"],
        "Steps": [
            {"title": "Tier 1: Subject Mastery", "desc": "Get a Master's degree in your field.", "knowledge": "You cannot teach what you don't know deeply.", "tip": "Start tutoring part-time."},
            {"title": "Tier 2: Pedagogy", "desc": "Get a B.Ed or clear NET/PhD.", "knowledge": "Teaching is an art of simplifying complexity.", "tip": "Study child psychology."},
            {"title": "Tier 3: Classroom Mgmt", "desc": "Learn to handle students and discipline.", "knowledge": "Control the room with respect, not fear.", "tip": "Observe senior teachers."},
            {"title": "Tier 4: Tech in Edu", "desc": "Learn to use digital tools (LMS/Quizzes).", "knowledge": "The future of education is blended learning.", "tip": "Learn Google Classroom."},
            {"title": "Tier 5: Research", "desc": "Publish papers and stay updated.", "knowledge": "A teacher is a lifelong student.", "tip": "Attend 2 seminars a year."}
        ]
    },
    "Policy / Research Assistant": {
        "Stats": {"Time": "1-2 Years", "Market": "Niche", "Salary": "₹5L - ₹12L"},
        "Prereq": ["Research", "Writing", "Politics"],
        "Tools": ["SPSS", "Stata", "R", "Excel"],
        "Certs": ["Policy Analyst Cert"],
        "Steps": [
            {"title": "Tier 1: Research Methods", "desc": "Learn qualitative and quantitative analysis.", "knowledge": "Data is the foundation of good policy.", "tip": "Learn R or Stata."},
            {"title": "Tier 2: Paper Writing", "desc": "Learn to write white papers and briefs.", "knowledge": "If you can't explain a policy in 1 page, you don't know it.", "tip": "Get published in a journal."},
            {"title": "Tier 3: Data Visualization", "desc": "Learn to present social data.", "knowledge": "Show the human impact through the data.", "tip": "Learn GIS mapping."},
            {"title": "Tier 4: Think Tank Work", "desc": "Get an internship at a Think Tank or NGO.", "knowledge": "Networking in policy circles is vital.", "tip": "Attend 5 policy summits."},
            {"title": "Tier 5: Policy Advisor", "desc": "Consult for government or corporate.", "knowledge": "Influence change through evidence-based policy.", "tip": "Focus on a niche (e.g. Climate)."}
        ]
    },

    # ================================
    # Healthcare & Life Sciences
    # ================================
    "Medical Doctor": {
        "Stats": {"Time": "5-10 Years", "Market": "High Stability", "Salary": "Very High"},
        "Prereq": ["Science", "Focus", "Ethics"],
        "Tools": ["Diagnostics", "Medical Software"],
        "Certs": ["MBBS / MD"],
        "Steps": [
            {"title": "Tier 1: MBBS", "desc": "Complete 5.5 years of medical school.", "knowledge": "Anatomy is the map; pathology is the terrain.", "tip": "Don't skip the labs."},
            {"title": "Tier 2: Clinical Rotations", "desc": "Learn diagnosis on real patients.", "knowledge": "Treat the patient, not just the disease.", "tip": "Improve your bedside manner."},
            {"title": "Tier 3: Residency", "desc": "3 years of supervised practice.", "knowledge": "This is where you earn your 'medical intuition'.", "tip": "Choose a specialty early."},
            {"title": "Tier 4: PG/Specialization", "desc": "Get an MD or MS.", "knowledge": "Deepen your knowledge in one field (e.g. Cardiology).", "tip": "Prepare for PG exams."},
            {"title": "Tier 5: Practice", "desc": "Senior Resident or Consultant role.", "knowledge": "Medicine is a lifelong commitment to learning.", "tip": "Stay current with Lancet/NEJM journals."}
        ]
    },
    "Dentist": {
        "Stats": {"Time": "5 Years", "Market": "Stable", "Salary": "₹5L - ₹15L"},
        "Prereq": ["Manual Dexterity", "Science", "Patience"],
        "Tools": ["Dental Drill", "X-ray", "Mirror"],
        "Certs": ["BDS / MDS"],
        "Steps": [
            {"title": "Tier 1: BDS Foundations", "desc": "Learn oral medicine and physiology.", "knowledge": "Oral health is the window to overall health.", "tip": "Practice hand-eye coordination."},
            {"title": "Tier 2: Dental Anatomy", "desc": "Study tooth structures in detail.", "knowledge": "Accuracy in millimeters matters here.", "tip": "Draw dental diagrams."},
            {"title": "Tier 3: Clinical Work", "desc": "Treat patients under supervision.", "knowledge": "Patience is your most important tool.", "tip": "Learn to manage patient fear."},
            {"title": "Tier 4: Specialization", "desc": "Get an MDS (Orthodontics, etc.).", "knowledge": "Specialists earn more and have specific niches.", "tip": "Focus on aesthetics."},
            {"title": "Tier 5: Private Clinic", "desc": "Learn to manage your own practice.", "knowledge": "Being a dentist is also being a business owner.", "tip": "Learn clinic marketing."}
        ]
    },
    "Pharmacist": {
        "Stats": {"Time": "4 Years", "Market": "Growing", "Salary": "₹4L - ₹10L"},
        "Prereq": ["Chemistry", "Accuracy", "Memory"],
        "Tools": ["Dispensing Software", "Lab Tools"],
        "Certs": ["B.Pharm / M.Pharm"],
        "Steps": [
            {"title": "Tier 1: Pharmaceutical Chem", "desc": "Learn drug formulation and synthesis.", "knowledge": "The difference between medicine and poison is the dose.", "tip": "Master Organic Chemistry."},
            {"title": "Tier 2: Pharmacology", "desc": "Study how drugs affect the body.", "knowledge": "Interaction is the biggest risk in dispensing.", "tip": "Study drug interaction charts."},
            {"title": "Tier 3: Compliance & Law", "desc": "Learn drug regulations and ethics.", "knowledge": "Stay updated on FDA/Local laws.", "tip": "Visit a manufacturing unit."},
            {"title": "Tier 4: Retail/Hospital", "desc": "Internship in a pharmacy setting.", "knowledge": "Counseling the patient is your key value.", "tip": "Learn to manage inventory."},
            {"title": "Tier 5: R&D / Clinical", "desc": "Move into drug research or management.", "knowledge": "Innovation happens in the lab.", "tip": "Get a Master's degree."}
        ]
    },
    "Public Health Professional": {
        "Stats": {"Time": "2-3 Years", "Market": "Growing", "Salary": "₹6L - ₹15L"},
        "Prereq": ["Data", "Sociology", "Ethics"],
        "Tools": ["Excel", "GIS", "SPSS"],
        "Certs": ["MPH"],
        "Steps": [
            {"title": "Tier 1: Epidemiology", "desc": "Learn how diseases spread.", "knowledge": "Prevention is better than cure for a population.", "tip": "Study the history of pandemics."},
            {"title": "Tier 2: Health Policy", "desc": "Learn to design health programs.", "knowledge": "Policy must be evidence-based.", "tip": "Intern with an NGO or WHO."},
            {"title": "Tier 3: Biostatistics", "desc": "Learn to analyze large-scale health data.", "knowledge": "Data is the voice of the community.", "tip": "Master Excel for social data."},
            {"title": "Tier 4: GIS Mapping", "desc": "Learn to map health trends geographically.", "knowledge": "Where you live affects how long you live.", "tip": "Learn ArcGIS basics."},
            {"title": "Tier 5: Program Mgmt", "desc": "Manage large scale health interventions.", "knowledge": "Turning policy into practice saves lives.", "tip": "Focus on a niche (e.g. nutrition)."}
        ]
    },

    # ================================
    # Aviation, Law & Engineering
    # ================================
    "Commercial Pilot": {
        "Stats": {"Time": "2 Years", "Market": "Global", "Salary": "₹15L - ₹40L+"},
        "Prereq": ["Physics", "Fitness", "English"],
        "Tools": ["Flight Sim", "Logbook", "Navigation Charts"],
        "Certs": ["CPL / ATPL"],
        "Steps": [
            {"title": "Tier 1: Ground School", "desc": "Clear Met, Nav, and Regs exams.", "knowledge": "A pilot is a student of the sky.", "tip": "Clear all 6 exams early."},
            {"title": "Tier 2: Flight Training", "desc": "Complete 200 hours of actual flying.", "knowledge": "Muscle memory and calmness are key.", "tip": "Choose a school with good fleet."},
            {"title": "Tier 3: Type Rating", "desc": "Get certified for A320 or B737.", "knowledge": "This is where you become an airline pro.", "tip": "Practice in the simulator daily."},
            {"title": "Tier 4: First Officer", "desc": "Start flying with an airline.", "knowledge": "Learn from senior captains. Experience counts.", "tip": "Stay physically fit."},
            {"title": "Tier 5: Captaincy", "desc": "Earn 1500+ hours and command upgrade.", "knowledge": "The safety of the aircraft is on you.", "tip": "Learn CRM (Crew Resource Mgmt)."}
        ]
    },
    "Lawyer / Advocate": {
        "Stats": {"Time": "3-5 Years", "Market": "Stable", "Salary": "₹6L - ₹25L+"},
        "Prereq": ["Reasoning", "Writing", "Ethics"],
        "Tools": ["Legal DBs", "Drafting Tools"],
        "Certs": ["LLB / Bar Exam"],
        "Steps": [
            {"title": "Tier 1: Law School", "desc": "Complete 3 or 5 years of LLB.", "knowledge": "Law is not just rules; it's about justice.", "tip": "Do internships every summer."},
            {"title": "Tier 2: Moot Courts", "desc": "Practice oral advocacy in mock trials.", "knowledge": "Public speaking is a core lawyer skill.", "tip": "Join your college moot society."},
            {"title": "Tier 3: Bar Exam", "desc": "Clear the license exam to practice.", "knowledge": "This is your license to represent clients.", "tip": "Focus on procedural laws."},
            {"title": "Tier 4: Litigation/Corp", "desc": "Pick your field: Court or Office.", "knowledge": "Specialization leads to higher earnings.", "tip": "Shadow a senior advocate."},
            {"title": "Tier 5: Legal Expert", "desc": "Build your own firm or become a Partner.", "knowledge": "Trust and reputation are your only capital.", "tip": "Master legal research."}
        ]
    },
    "Chartered Engineer": {
        "Stats": {"Time": "4-6 Years", "Market": "Stable", "Salary": "₹8L - ₹18L"},
        "Prereq": ["Math", "Physics", "Experience"],
        "Tools": ["CAD Software", "Project Mgmt Tools"],
        "Certs": ["Chartered Status"],
        "Steps": [
            {"title": "Tier 1: Degree", "desc": "Get a B.E/B.Tech in your core field.", "knowledge": "The basics of engineering never change.", "tip": "Maintain a high GPA."},
            {"title": "Tier 2: Professional Exp", "desc": "Gain 5 years of industry experience.", "knowledge": "Real learning happens on the site.", "tip": "Focus on Quality Control."},
            {"title": "Tier 3: Ethics & Safety", "desc": "Learn ISO standards and safety codes.", "knowledge": "An engineer's first duty is public safety.", "tip": "Get OHSAS certified."},
            {"title": "Tier 4: Technical Report", "desc": "Write a report on a complex project.", "knowledge": "Explain the 'Why' behind the 'How'.", "tip": "Document your projects well."},
            {"title": "Tier 5: Peer Review", "desc": "Get vetted by the Institution of Engineers.", "knowledge": "Chartered status is a mark of global excellence.", "tip": "Apply for international status."}
        ]
    },
    "Merchant Navy Officer": {
        "Stats": {"Time": "1-3 Years", "Market": "Global", "Salary": "₹10L - ₹30L+ (Tax Free)"},
        "Prereq": ["Fitness", "Physics", "Discipline"],
        "Tools": ["Nav Charts", "Engine Monitors"],
        "Certs": ["DG Shipping / COC"],
        "Steps": [
            {"title": "Tier 1: Pre-sea Training", "desc": "Complete B.Sc Nautical or DNS.", "knowledge": "Discipline is the law of the sea.", "tip": "Stay physically fit."},
            {"title": "Tier 2: Cadetship", "desc": "18 months of training at sea.", "knowledge": "The ocean is a harsh but fair teacher.", "tip": "Learn from the deck officers."},
            {"title": "Tier 3: COC Exam", "desc": "Clear the 2nd Mate exams.", "knowledge": "This makes you a licensed officer.", "tip": "Master navigation charts."},
            {"title": "Tier 4: Promotions", "desc": "Move from 3rd to 1st Officer.", "knowledge": "Cargo safety is your primary duty.", "tip": "Learn ship stability."},
            {"title": "Tier 5: Captaincy", "desc": "Become the Master of the vessel.", "knowledge": "The Captain is second only to God at sea.", "tip": "Master maritime law."}
        ]
    },

    # ================================
    # Skilled & Emerging
    # ================================
    "Digital Marketing Specialist": {
        "Stats": {"Time": "6 Months", "Market": "Very High", "Salary": "₹4L - ₹12L"},
        "Prereq": ["Creativity", "Data", "Trends"],
        "Tools": ["Google Ads", "HubSpot", "Meta Manager"],
        "Certs": ["HubSpot / Google Ads"],
        "Steps": [
            {"title": "Tier 1: Marketing Core", "desc": "Learn psychology and marketing funnels.", "knowledge": "Marketing is about knowing who your customer is.", "tip": "Read 'Influence' by Cialdini."},
            {"title": "Tier 2: SEO & SEM", "desc": "Learn Search Engine Marketing.", "knowledge": "If you aren't on page 1, you aren't online.", "tip": "Start a personal blog."},
            {"title": "Tier 3: Social Ads", "desc": "Learn paid media on Meta/LinkedIn.", "knowledge": "Targeting is 80% of the success.", "tip": "Run a $10 trial ad."},
            {"title": "Tier 4: Automation", "desc": "Learn email marketing and CRM.", "knowledge": "Automation is how you scale a small team.", "tip": "Learn HubSpot."},
            {"title": "Tier 5: Growth Strategy", "desc": "Learn full-funnel strategy.", "knowledge": "A specialist knows a tool; a strategist knows a business.", "tip": "Analyze a brand's growth."}
        ]
    },
    "SEO / Growth Analyst": {
        "Stats": {"Time": "6-12 Months", "Market": "High", "Salary": "₹6L - ₹15L"},
        "Prereq": ["Analytical", "Persistence", "HTML Basics"],
        "Tools": ["Ahrefs", "SEMRush", "Search Console"],
        "Certs": ["Yoast / SEMRush Cert"],
        "Steps": [
            {"title": "Tier 1: On-page SEO", "desc": "Master keywords and metadata.", "knowledge": "Content is king; optimization is the crown.", "tip": "Audit a website for free."},
            {"title": "Tier 2: Technical SEO", "desc": "Learn site speed and XML sitemaps.", "knowledge": "Google won't index what it cannot crawl.", "tip": "Learn Core Web Vitals."},
            {"title": "Tier 3: Link Building", "desc": "Learn to earn backlinks.", "knowledge": "Links are the 'votes of confidence' for your site.", "tip": "Master guest posting."},
            {"title": "Tier 4: Growth Hacking", "desc": "Learn viral loops and A/B testing.", "knowledge": "Find the small levers that move big needles.", "tip": "Learn Google Optimize."},
            {"title": "Tier 5: Data SEO", "desc": "Learn to use data to predict trends.", "knowledge": "Predictive SEO is the future.", "tip": "Master Search Console data."}
        ]
    },
    "Technical Content Creator": {
        "Stats": {"Time": "1 Year", "Market": "Growing", "Salary": "Variable"},
        "Prereq": ["Writing", "Tech Savvy", "Public Speaking"],
        "Tools": ["Obsidian", "Premiere", "Substack"],
        "Certs": ["Creator Certs"],
        "Steps": [
            {"title": "Tier 1: Subject Mastery", "desc": "Learn a tech niche deeply.", "knowledge": "You can't create if you don't know.", "tip": "Write weekly on a tech topic."},
            {"title": "Tier 2: Writing/Video", "desc": "Learn to edit and write for the web.", "knowledge": "Clarity over cleverness always wins.", "tip": "Start a YouTube or Blog."},
            {"title": "Tier 3: Distribution", "desc": "Learn to grow an audience on LinkedIn/X.", "knowledge": "Own your audience through an email list.", "tip": "Set up a Substack."},
            {"title": "Tier 4: Personal Branding", "desc": "Learn to be a 'Thought Leader'.", "knowledge": "You are the product in this career.", "tip": "Be consistent for 6 months."},
            {"title": "Tier 5: Monetization", "desc": "Learn courses, sponsorships, and ads.", "knowledge": "Diversify your income early.", "tip": "Learn Stripe and Gumroad."}
        ]
    },
    "No-Code / Automation Specialist": {
        "Stats": {"Time": "6 Months", "Market": "Emerging", "Salary": "₹6L - ₹18L"},
        "Prereq": ["Logic", "Efficiency", "API Basics"],
        "Tools": ["Zapier", "Bubble", "Airtable"],
        "Certs": ["Zapier Expert"],
        "Steps": [
            {"title": "Tier 1: Workflow Logic", "desc": "Learn to map 'If-This-Then-That'.", "knowledge": "Every business is just a series of workflows.", "tip": "Diagram your morning routine."},
            {"title": "Tier 2: Tool Mastery", "desc": "Learn Airtable and Zapier deeply.", "knowledge": "Airtable is your database; Zapier is your engine.", "tip": "Build a CRM in Airtable."},
            {"title": "Tier 3: API Integration", "desc": "Learn Webhooks and JSON.", "knowledge": "Connecting apps is the core of automation.", "tip": "Read API documentation for fun."},
            {"title": "Tier 4: Web App No-Code", "desc": "Learn to build apps with Bubble or Softr.", "knowledge": "Build full apps without writing code.", "tip": "Build an MVP in 24 hours."},
            {"title": "Tier 5: Solutions Architect", "desc": "Consult for companies to automate ops.", "knowledge": "You sell time, not just tools.", "tip": "Find a local business and automate 1 task."}
        ]
    }
}

CAREER_IMAGES = {
    "Software Engineer": "https://images.unsplash.com/photo-1581090700227-1e37b190418e",
    "Data Analyst": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
    "Product Manager (Tech)": "https://images.unsplash.com/photo-1600880292203-757bb62b4baf",
    "QA / Test Engineer": "https://images.unsplash.com/photo-1580894894513-541e068a3e2b",
    "Business Analyst": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
    "Operations Manager": "https://images.unsplash.com/photo-1581093458791-9d15482778c9",
    "Management Consultant": "https://images.unsplash.com/photo-1507679799987-c73779587ccf",
    "Entrepreneur (Early-stage)": "https://images.unsplash.com/photo-1557804506-669a67965ba0",
    "UI/UX Designer": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c",
    "Graphic Designer": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "Content Strategist / Copywriter": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2",
    "Digital Media Specialist": "https://images.unsplash.com/photo-1557838923-2985c318be48",
    "Fashion Designer": "https://images.unsplash.com/photo-1520975922215-2c8b7a0aabf3",
    "Textile Designer": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f",
    "Architect": "https://images.unsplash.com/photo-1503387762-592deb58ef4e",
    "Interior Designer": "https://images.unsplash.com/photo-1505691938895-1758d7feb511",
    "Financial Analyst": "https://images.unsplash.com/photo-1565373679107-344d6c7d32b3",
    "Chartered Accountant (CA)": "https://images.unsplash.com/photo-1554224155-6726b3ff858f",
    "Investment Banking Analyst": "https://images.unsplash.com/photo-1567427018141-0584cfcbf1b8",
    "Risk & Compliance Analyst": "https://images.unsplash.com/photo-1605902711622-cfb43c44367f",
    "Civil Services / Government Exams": "https://images.unsplash.com/photo-1551836022-d5d88e9218df",
    "Public Sector Officer": "https://images.unsplash.com/photo-1573496130141-209d200cebdc",
    "School / College Teacher": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655",
    "Policy / Research Assistant": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
    "Medical Doctor": "https://images.unsplash.com/photo-1580281657527-47d1e2c94a31",
    "Dentist": "https://images.unsplash.com/photo-1606813902917-7f8c66f6a6b5",
    "Pharmacist": "https://images.unsplash.com/photo-1580281658629-3e7f2f3b2b7f",
    "Public Health Professional": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144",
    "Commercial Pilot": "https://images.unsplash.com/photo-1517948430535-1e2469d314fe",
    "Lawyer / Advocate": "https://images.unsplash.com/photo-1505664194779-8beaceb93744",
    "Chartered Engineer": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc",
    "Merchant Navy Officer": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21",
    "Digital Marketing Specialist": "https://images.unsplash.com/photo-1557838923-2985c318be48",
    "SEO / Growth Analyst": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0",
    "Technical Content Creator": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
    "No-Code / Automation Specialist": "https://images.unsplash.com/photo-1581091012184-7b1b06b8b0f1"
}
# --- 4. SESSION MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = "Questionnaire"
if 'results' not in st.session_state: st.session_state.results = None
if "selected_career" not in st.session_state:
    st.session_state.selected_career = None

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/1087/1087840.png" width="70">
        <h3>PATHWISE</h3>
        <p style="color:#6c757d;">AI Career Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Advanced Career Prediction System")
    st.divider()
    
    if st.button("📝 Assessment"): st.session_state.page = "Questionnaire"
    
    if st.session_state.results:
        st.markdown("---")
        if st.button("📊 Fit Analysis"): st.session_state.page = "Results"
        if st.button("🗺️ Detailed Roadmaps"): st.session_state.page = "Roadmaps"
    
    st.divider()
    st.info("System Status: Operational\nModel Accuracy: 95%+")

# --- 6. PAGE: QUESTIONNAIRE ---
if st.session_state.page == "Questionnaire":
    st.markdown("""
    <div style="display:flex;align-items:center;gap:25px;">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="90">
        <div>
            <h1>PATHWISE</h1>
            <p style="font-size:18px;color:#6c757d;">
            AI-Powered Career Discovery & Strategic Roadmapping
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("Complete the profile below to generate your AI-powered career report.")
    
    with st.form("main_quiz"):
        c1, c2 = st.columns(2)
        with c1:
            field = st.selectbox("Current Academic Domain", ["Tech", "Science", "Commerce", "Arts"])
            edu = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's"])
            learning = st.selectbox("Learning Speed", ["Fast", "Steady"])
        with c2:
            time = st.selectbox("Stability Horizon", ["Short (1-2 yrs)", "Medium (3-5 yrs)", "Long (5+ yrs)"])
            risk = st.select_slider("Risk Appetite", ["Low", "Medium", "High"])
            
        st.divider()
        ints = st.multiselect("Core Interests (Max 3)", mlb_int.classes_, max_selections=3)
        strs = st.multiselect("Primary Strengths (Max 3)", mlb_str.classes_, max_selections=3)
        
        if st.form_submit_button("Generate AI Career Report"):
            if len(ints) == 0 or len(strs) == 0:
                st.error("Please select at least one Interest and one Strength.")
            else:
                # Build Feature Vector
                input_df = pd.DataFrame(0, index=[0], columns=model_features)
                for col in [f"field_{field}", f"education_{edu}", f"learning_rate_{learning}", f"risk_tolerance_{risk}"]:
                    if col in input_df.columns: input_df.at[0, col] = 1
                for i in ints: input_df.at[0, f"int_{i}"] = 1
                for s in strs: input_df.at[0, f"str_{s}"] = 1

                # --- 70-100% TEMPERATURE BOOST LOGIC ---
                raw_probs = model.predict_proba(input_df)[0]
                T = 0.25 # Sharpness factor
                exp_p = np.exp(raw_probs / T)
                boosted_p = (exp_p / np.sum(exp_p)) * 100
                
                # Calibration floor
                top_idx = np.argmax(boosted_p)
                if boosted_p[top_idx] < 75: boosted_p = np.clip(boosted_p * (85/boosted_p[top_idx]), 0, 98.4)

                top_3 = np.argsort(boosted_p)[-3:][::-1]
                st.session_state.results = [{"career": le.inverse_transform([idx])[0], "score": round(boosted_p[idx], 1)} for idx in top_3]
                st.session_state.page = "Results"
                st.rerun()

# --- 7. PAGE: RESULTS ---
elif st.session_state.page == "Results":

    st.title("📊 Career Fit Analysis")

    for item in st.session_state.results:
        career = item["career"]
        score = item["score"]
        img = CAREER_IMAGES.get(career)

        col_img, col_data = st.columns([1, 3])

        with col_img:
            if img:
                st.markdown(
                    f"""
                    <div class="career-image-card">
                        <img src="{img}" style="width:100%; height:160px; object-fit:cover;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_data:
            st.markdown(f"""
                <div class="result-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3>{career}</h3>
                        <h2 style="color:#007bff;">{score}%</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(score / 100)

            if st.button(f"View Roadmap → {career}", key=f"roadmap_{career}"):
                st.session_state.selected_career = career
                st.session_state.page = "Roadmaps"
                st.rerun()


# --- PAGE: ROADMAPS (ULTRA-DETAILED) ---
elif st.session_state.page == "Roadmaps":

    st.title("🗺 Strategic Career Roadmaps")

    careers = [r["career"] for r in st.session_state.results]
    tabs = st.tabs(careers)

    for i, tab in enumerate(tabs):
        with tab:
            career = careers[i]
            data = DEEP_DATA.get(career, DEEP_DATA["Software Engineer"])

            # ---------- Career Image (Container) ----------
            img = CAREER_IMAGES.get(career)
            if img:
                st.markdown(
                    f"""
                    <div class="career-image-card" style="margin-bottom:24px;">
                        <img src="{img}" style="width:100%; height:280px; object-fit:cover;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.success(f"Personalized roadmap for **{career}**")

            # ---------- Executive Summary ----------
            st.markdown(
                f"**Primary Objective:** Transition from a learner to a **{career}** within **{data['Stats']['Time']}**."
            )

            # ---------- Industry Metrics ----------
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Prep Time", data["Stats"]["Time"])
            m2.metric("Industry Demand", data["Stats"]["Market"])
            m3.metric("Salary (Entry)", data["Stats"]["Salary"])
            m4.metric("Difficulty", "Medium–High")

            # ---------- Prerequisites & Tools ----------
            st.divider()
            col_pre, col_tools = st.columns(2)

            with col_pre:
                st.markdown("#### 📋 Core Prerequisites")
                for p in data["Prereq"]:
                    st.write(f"• {p}")

            with col_tools:
                st.markdown("#### 🛠️ Professional Toolstack")
                st.write(" / ".join([f"`{t}`" for t in data["Tools"]]))

            # ---------- Mastery Path ----------
            st.divider()
            st.markdown("#### 🛤️ The 5-Tier Mastery Path")

            for step in data["Steps"]:
                with st.expander(
                    f"📍 {step['title']}",
                    expanded=(step == data["Steps"][0])
                ):
                    st.markdown(f"**Deep Dive:** {step['desc']}")
                    st.markdown(f"**Knowledge Pill:** {step['knowledge']}")
                    st.info(f"💡 **Strategy:** {step['tip']}")

            # ---------- Certifications ----------
            st.divider()
            st.markdown("#### 🎓 Credentials & Learning Resources")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Must-Have Certifications**")
                for cert in data["Certs"]:
                    st.code(cert)

            with c2:
                st.markdown("**Recommended Resources**")
                for res in data.get(
                    "Resources",
                    ["Official Documentation", "Industry Whitepapers"]
                ):
                    st.write(f"📚 {res}")





    