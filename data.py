import pandas as pd
import random

# Advanced Logic: (Core_Interests, Affinity_Interests, Primary_Strengths, Secondary_Strengths, Preferred_Field)
logic_map = {
    # Technology
    "Software Engineer": (["Coding", "Tech"], ["Logic", "Math", "APIs"], ["Problem Solving"], ["Focus", "Adaptability"], "Tech"),
    "Data Analyst": (["Analysis", "Statistics"], ["Math", "Excel", "SQL"], ["Logic"], ["Attention to Detail", "Focus"], "Tech"),
    "Product Manager (Tech)": (["Management", "Tech"], ["Strategy", "UX", "Business"], ["Leadership"], ["Communication", "Empathy"], "Tech"),
    "QA / Test Engineer": (["Tech", "Automation"], ["Details", "Software", "Logic"], ["Patience"], ["Attention to Detail", "Focus"], "Tech"),
    
    # Business
    "Business Analyst": (["Analysis", "Business"], ["Strategy", "Documentation", "Finance"], ["Logic"], ["Communication", "Organization"], "Commerce"),
    "Operations Manager": (["Management", "Supply Chain"], ["Optimization", "Strategy", "Business"], ["Leadership"], ["Organization", "Resilience"], "Commerce"),
    "Management Consultant": (["Strategy", "Analysis"], ["Public Speaking", "Case Studies"], ["Communication"], ["Problem Solving", "Adaptability"], "Commerce"),
    "Entrepreneur (Early-stage)": (["Innovation", "Business"], ["Risk Taking", "Sales", "Strategy"], ["Leadership"], ["Resilience", "Adaptability"], "Any"),
    
    # Design
    "UI/UX Designer": (["Design", "Psychology"], ["Wireframing", "Tech", "Art"], ["Empathy"], ["Creativity", "Visual Thinking"], "Tech"),
    "Graphic Designer": (["Art", "Design"], ["Typography", "Visuals", "Creativity"], ["Creativity"], ["Visual Thinking", "Attention to Detail"], "Arts"),
    "Content Strategist / Copywriter": (["Writing", "Marketing"], ["SEO", "Social Media", "Storytelling"], ["Communication"], ["Creativity", "Adaptability"], "Arts"),
    "Digital Media Specialist": (["Social Media", "Video"], ["Editing", "Marketing", "Content"], ["Creativity"], ["Adaptability", "Communication"], "Arts"),

    # Architecture/Fashion
    "Fashion Designer": (["Fashion", "Art"], ["Textiles", "Sketching", "Trends"], ["Creativity"], ["Attention to Detail", "Visual Thinking"], "Arts"),
    "Textile Designer": (["Textiles", "Art"], ["Fabric Science", "Patterns"], ["Creativity"], ["Technical Knowledge", "Patience"], "Arts"),
    "Architect": (["Architecture", "Math"], ["Design", "Physics", "Drafting"], ["Visual Thinking"], ["Focus", "Logic"], "Science"),
    "Interior Designer": (["Design", "Aesthetics"], ["Space Planning", "Decor", "Art"], ["Creativity"], ["Empathy", "Visual Thinking"], "Arts"),

    # Finance
    "Financial Analyst": (["Finance", "Analysis"], ["Stock Market", "Math", "Excel"], ["Logic"], ["Attention to Detail", "Focus"], "Commerce"),
    "Chartered Accountant (CA)": (["Accounting", "Finance"], ["Taxation", "Law", "Audit"], ["Attention to Detail"], ["Memory", "Patience"], "Commerce"),
    "Investment Banking Analyst": (["Finance", "Economics"], ["M&A", "Strategy", "Valuation"], ["Resilience"], ["Focus", "Logic"], "Commerce"),
    "Risk & Compliance Analyst": (["Finance", "Law"], ["Risk Modeling", "Ethics", "Audit"], ["Logic"], ["Attention to Detail", "Organization"], "Commerce"),

    # Public Service
    "Civil Services / Government Exams": (["Public Service", "History"], ["Governance", "Law", "Ethics"], ["Leadership"], ["Memory", "Patience"], "Any"),
    "Public Sector Officer": (["Administration", "Public Service"], ["Policy", "Management"], ["Organization"], ["Patience", "Communication"], "Any"),
    "School / College Teacher": (["Teaching", "Education"], ["Public Speaking", "Mentoring"], ["Communication"], ["Patience", "Memory"], "Any"),
    "Policy / Research Assistant": (["Research", "Politics"], ["Writing", "Data", "Sociology"], ["Focus"], ["Logic", "Attention to Detail"], "Arts"),

    # Healthcare
    "Medical Doctor": (["Biology", "Medicine"], ["Science", "Anatomy", "Ethics"], ["Empathy"], ["Memory", "Resilience"], "Science"),
    "Dentist": (["Biology", "Healthcare"], ["Manual Dexterity", "Science"], ["Attention to Detail"], ["Empathy", "Patience"], "Science"),
    "Pharmacist": (["Chemistry", "Medicine"], ["Pharmacology", "Details", "Science"], ["Memory"], ["Attention to Detail", "Organization"], "Science"),
    "Public Health Professional": (["Science", "Sociology"], ["Data", "Epidemiology", "Policy"], ["Communication"], ["Empathy", "Adaptability"], "Science"),

    # Aviation/Law/Eng
    "Commercial Pilot": (["Aviation", "Travel"], ["Physics", "Geography", "Navigation"], ["Focus"], ["Physical Fitness", "Resilience"], "Science"),
    "Lawyer / Advocate": (["Law", "Writing"], ["Critical Reasoning", "Public Speaking", "History"], ["Communication"], ["Logic", "Memory"], "Arts"),
    "Chartered Engineer": (["Engineering", "Physics"], ["Math", "Problem Solving", "Tech"], ["Logic"], ["Focus", "Technical Knowledge"], "Science"),
    "Merchant Navy Officer": (["Navigation", "Travel"], ["Marine Science", "Mechanics"], ["Resilience"], ["Physical Fitness", "Leadership"], "Science"),

    # Emerging
    "Digital Marketing Specialist": (["Marketing", "Social Media"], ["SEO", "Ads", "Content"], ["Adaptability"], ["Creativity", "Communication"], "Commerce"),
    "SEO / Growth Analyst": (["Analysis", "Marketing"], ["Tech", "Data", "Keywords"], ["Logic"], ["Attention to Detail", "Adaptability"], "Tech"),
    "Technical Content Creator": (["Writing", "Tech"], ["Blogging", "Video", "Education"], ["Communication"], ["Creativity", "Technical Knowledge"], "Tech"),
    "No-Code / Automation Specialist": (["Tech", "Optimization"], ["Workflows", "APIs", "Logic"], ["Problem Solving"], ["Adaptability", "Logic"], "Tech")
}

data = []
for career, (core_i, aff_i, pri_s, sec_s, field) in logic_map.items():
    for _ in range(100):
        # 1. Interests: Core is always present, plus random logical affinities
        selected_ints = list(set(core_i + random.sample(aff_i, random.randint(1, 2))))
        
        # 2. Strengths: Primary is always present, plus logical secondaries
        selected_strs = list(set(pri_s + random.sample(sec_s, 1)))
        
        # 3. Decision Logic for other features
        row = {
            "career": career,
            "interests": ", ".join(selected_ints),
            "strengths": ", ".join(selected_strs),
            "field": field if random.random() > 0.15 else random.choice(["Science", "Commerce", "Arts", "Tech"]),
            "education": "Master's" if career in ["Medical Doctor", "Management Consultant", "Public Health Professional"] else "Bachelor's",
            "learning_rate": "Fast" if "Tech" in field or "Science" in field else "Steady",
            "time_horizon": "Long (5+ yrs)" if career in ["Medical Doctor", "Architect", "Chartered Engineer"] else "Short (1-2 yrs)",
            "risk_tolerance": "High" if career in ["Entrepreneur (Early-stage)", "Commercial Pilot", "Investment Banking Analyst"] else random.choice(["Low", "Medium"])
        }
        data.append(row)

df = pd.DataFrame(data)
df.to_csv('newdata.csv', index=False)
print("Sophisticated Logic Dataset 'pd2.csv' ready!")