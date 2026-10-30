"""
Debris Careers - NLP + Machine Learning Career Recommendation Engine
Combines:
1. TF-IDF Vectorization & Cosine Similarity for personalized ML recommendation.
2. Rule-based structured knowledge retrieval (Colleges, Courses, Hiring Companies, Next Steps).
3. Conversational Profiler (Extracts Interests, Skills, Work Style & Priority: Salary/Impact/Creativity/Stability).
100% Offline, Local ML with scikit-learn & pandas.
"""

import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# 1. Comprehensive Structured Careers Dataset
# ---------------------------------------------------------------------------
CAREERS_DATA = [
    {
        "id": "data_scientist",
        "title": "Data Scientist / Machine Learning Engineer",
        "stream": "non_medical",
        "level": "Graduation & Masters",
        "description": "Applies mathematics, statistical modeling, machine learning, and computer programming to extract intelligence from complex datasets, build predictive AI systems, and guide high-stakes business strategy.",
        "interests": "mathematics, computers, machine learning, artificial intelligence, statistics, algorithms, logical reasoning, data analysis, deep learning, prediction",
        "skills": "Python, SQL, Probability, Machine Learning, Data Visualization, Problem Solving",
        "priorities": "salary, high paying, innovation, analytical problem solving, intellectual challenge",
        "education": "B.Tech in Computer Science / AI / Data Science, B.Sc Statistics, M.Tech / MS in Data Science",
        "colleges": [
            "Indian Statistical Institute (ISI) Kolkata / Delhi",
            "IIT Bombay, IIT Delhi, IIT Madras, IIT Kharagpur",
            "IIIT Hyderabad & BITS Pilani",
            "IISc Bangalore"
        ],
        "top_fields": [
            "Predictive Modeling & Generative AI",
            "Computer Vision & Deep Learning",
            "Quantitative Algorithmic Trading",
            "Big Data Infrastructure & Pipeline Engineering"
        ],
        "companies": [
            "Google DeepMind, Microsoft Research, NVIDIA",
            "Amazon, Meta, Apple",
            "WorldQuant, Tower Research Capital, Goldman Sachs",
            "Fractal Analytics, Mu Sigma"
        ],
        "recommended_next_steps": [
            "Master Python and essential libraries (NumPy, Pandas, Scikit-Learn)",
            "Build strong foundations in Linear Algebra, Probability, and Multivariate Calculus",
            "Learn SQL and database querying for real-world datasets",
            "Create end-to-end data analysis and machine learning portfolio projects on Kaggle or GitHub",
            "Prepare for engineering entrance tests (JEE Main/Advanced, ISI Admission Test)"
        ]
    },
    {
        "id": "software_engineer",
        "title": "Software Development Engineer (SDE / Systems Architect)",
        "stream": "non_medical",
        "level": "Graduation",
        "description": "Designs, develops, tests, and architects scalable software systems, web applications, cloud infrastructure, and low-latency distributed systems.",
        "interests": "coding, computers, software, web development, app development, algorithms, system design, problem solving, technology, building products",
        "skills": "Data Structures, Algorithms, Python, Java, C++, Cloud Platforms (AWS/GCP), System Design",
        "priorities": "salary, job stability, high paying, career growth, building technology",
        "education": "B.Tech / B.E. in Computer Science & Engineering, BCA + MCA",
        "colleges": [
            "IIT Bombay, IIT Delhi, IIT Kanpur, IIT Madras",
            "BITS Pilani (Pilani, Goa, Hyderabad)",
            "IIIT Hyderabad & IIIT Bangalore",
            "NIT Trichy & NIT Surathkal",
            "Delhi Technological University (DTU)"
        ],
        "top_fields": [
            "Full-Stack Web & Distributed Cloud Systems",
            "High-Performance Computing & Low-Latency Architecture",
            "Mobile Application Engineering (iOS/Android)",
            "DevOps, SRE & Cloud Infrastructure"
        ],
        "companies": [
            "Google, Microsoft, Amazon",
            "Meta, Uber, Apple, Netflix",
            "Atlassian, Adobe, Salesforce",
            "Directi, DE Shaw, Arcesium"
        ],
        "recommended_next_steps": [
            "Choose a core language: C++, Java, or Python, and master fundamentals",
            "Solve Data Structures & Algorithms problems consistently on LeetCode / Codeforces",
            "Build and deploy full-stack or backend web applications on the cloud",
            "Learn Git version control and contribute to open-source software",
            "Target JEE Main / BITSAT for top tech institute admissions"
        ]
    },
    {
        "id": "cybersecurity_analyst",
        "title": "Cybersecurity Analyst & Ethical Hacker",
        "stream": "non_medical",
        "level": "Graduation",
        "description": "Protects digital networks, computer infrastructure, cloud systems, and confidential intelligence from cyber attacks, vulnerabilities, and espionage.",
        "interests": "computers, security, ethical hacking, cyber defense, investigation, cryptography, forensics, network defense, curiosity",
        "skills": "Network Security, Penetration Testing, Linux, Cryptography, Wireshark, SIEM",
        "priorities": "job stability, salary, impact, high paying, intelligence, defense",
        "education": "B.Tech in Computer Science / Cybersecurity, B.Sc IT / Cyber Defense, Certifications (CEH, OSCP)",
        "colleges": [
            "IIT Delhi, IIT Kanpur (C3i Cybersecurity Hub)",
            "National Forensic Sciences University (NFSU), Gandhinagar",
            "BITS Pilani",
            "IIIT Delhi"
        ],
        "top_fields": [
            "Red Teaming & Offensive Penetration Testing",
            "Blue Teaming, Incident Response & SOC Operations",
            "Cloud Security & Zero-Trust Architecture",
            "Digital Forensics & Malware Analysis"
        ],
        "companies": [
            "Palo Alto Networks, CrowdStrike, FireEye",
            "Cisco Systems, Cloudflare",
            "Deloitte, PwC, EY, KPMG (Cyber Advisory)",
            "National Cyber Security Agencies, Intelligence Wings"
        ],
        "recommended_next_steps": [
            "Understand computer networking basics (TCP/IP, OSI, DNS, routing)",
            "Set up a Linux home lab and experiment with tools like Nmap, Wireshark, and Burp Suite",
            "Practice ethical hacking on platforms like TryHackMe and HackTheBox",
            "Earn industry entry certifications like CompTIA Security+ or Certified Ethical Hacker (CEH)",
            "Pursue B.Tech CSE or specialised Cybersecurity engineering degrees"
        ]
    },
    {
        "id": "chartered_accountant",
        "title": "Chartered Accountant (CA) & Corporate Financial Controller",
        "stream": "commerce",
        "level": "Graduation & Professional",
        "description": "Manages corporate financial auditing, tax compliance, corporate restructuring, forensic balance sheet examination, and statutory financial governance.",
        "interests": "accounts, accounting, mathematics, balance sheet, tax, taxation, auditing, audit, finance, corporate law, business numbers, precision",
        "skills": "Auditing, Financial Accounting, GST/Direct Taxation, Financial Modeling, Analytical Precision",
        "priorities": "salary, prestige, high paying, job stability, corporate authority",
        "education": "ICAI Qualification (Foundation, Inter, Articleship, Final) concurrently with B.Com (Hons)",
        "colleges": [
            "Institute of Chartered Accountants of India (ICAI - Governing Body)",
            "SRCC (Shri Ram College of Commerce), Delhi University",
            "Loyola College, Chennai",
            "St. Xavier's College, Kolkata / Mumbai"
        ],
        "top_fields": [
            "Statutory & Forensic Financial Auditing",
            "International Taxation, Transfer Pricing & GST",
            "Mergers & Acquisitions (M&A) Due Diligence",
            "Chief Financial Officer (CFO) Advisory"
        ],
        "companies": [
            "Deloitte, PwC, EY, KPMG (The Big Four Accounting Giants)",
            "BDO & Grant Thornton",
            "Goldman Sachs, Morgan Stanley",
            "Reliance Industries, Tata Sons, Aditya Birla Group"
        ],
        "recommended_next_steps": [
            "Register for the ICAI CA Foundation examination right after Class 12",
            "Enroll in B.Com (Hons) at a premier commerce university via CUET",
            "Master double-entry bookkeeping, corporate financial accounting, and tax codes",
            "Complete the mandatory 2-year practical articleship training with an accredited firm",
            "Clear CA Final to earn the prestigious fellowship qualification"
        ]
    },
    {
        "id": "investment_banker",
        "title": "Investment Banker & Equity Research Analyst",
        "stream": "commerce",
        "level": "Graduation & Masters",
        "description": "Advises Fortune 500 corporations, institutions, and governments on initial public offerings (IPOs), multi-billion-dollar mergers, corporate debt raising, and stock valuation.",
        "interests": "finance, stock market, investment, trading, equity, wall street, banking, valuation, mergers, acquisitions, economy, money, business",
        "skills": "Financial Modeling, DCF Valuation, Pitchbook Design, Corporate Finance, Excel mastery",
        "priorities": "salary, high paying, prestige, wealth, rapid career progression",
        "education": "B.Com (Hons) / B.A. Economics & MBA Finance / CFA (Chartered Financial Analyst)",
        "colleges": [
            "IIM Ahmedabad, IIM Bangalore, IIM Calcutta",
            "SRCC Delhi University",
            "FMS Delhi & XLRI Jamshedpur",
            "Global B-Schools: Wharton, Harvard, Columbia"
        ],
        "top_fields": [
            "Mergers & Acquisitions (M&A) Advisory",
            "Equity & Debt Capital Markets (ECM/DCM)",
            "Private Equity & Venture Capital Evaluation",
            "Equity Research & Industry Coverage"
        ],
        "companies": [
            "Goldman Sachs, Morgan Stanley, JP Morgan Chase",
            "Bank of America Merrill Lynch, Barclays, Citi",
            "Blackstone, KKR, Sequoia Capital / Peak XV",
            "Avendus Capital, Kotak Investment Banking"
        ],
        "recommended_next_steps": [
            "Learn Financial Modeling (Discounted Cash Flow, Comparable Company Analysis) in Excel",
            "Follow capital market trends, corporate earnings calls, and Bloomberg/FT reports daily",
            "Aim for premier undergraduate colleges (SRCC, St. Stephen's, IITs) via CUET or JEE",
            "Prepare for the CFA Level 1 exam and competitive MBA entrance tests (CAT / GMAT)",
            "Build an internship track record in boutique financial advisory or venture funds"
        ]
    },
    {
        "id": "medical_physician",
        "title": "Medical Physician / Surgeon",
        "stream": "medical",
        "level": "Graduation & Residency",
        "description": "Diagnoses clinical diseases, performs life-saving surgeries, manages trauma care, and provides patient healthcare in clinical settings and tertiary super-speciality hospitals.",
        "interests": "biology, human body, medicine, doctor, cure, disease, surgery, healing, hospital, patient, healthcare, science, empathy",
        "skills": "Clinical Diagnosis, Surgical Precision, Emergency Care, Pharmacology, Empathy",
        "priorities": "impact, helping people, job stability, prestige, salary, noble profession",
        "education": "MBBS (Bachelor of Medicine & Surgery) + MD/MS / DM/M.Ch Super-specialization",
        "colleges": [
            "AIIMS (All India Institute of Medical Sciences), New Delhi",
            "Christian Medical College (CMC), Vellore",
            "Armed Forces Medical College (AFMC), Pune",
            "JIPMER Puducherry & KGMU Lucknow"
        ],
        "top_fields": [
            "Interventional Cardiology & Cardiac Surgery",
            "Neurosurgery & Clinical Neurology",
            "Oncology (Medical & Surgical Cancer Care)",
            "Radio-Diagnosis, CT/MRI & Interventional Radiology"
        ],
        "companies": [
            "Apollo Hospitals Enterprise",
            "Max Super Speciality Hospitals",
            "Fortis Healthcare, Medanta - The Medicity",
            "World Health Organization (WHO), Red Cross"
        ],
        "recommended_next_steps": [
            "Focus intensively on Biology, Chemistry, and Physics in high school",
            "Prepare for the national NEET-UG medical entrance examination",
            "Complete 4.5 years of medical curriculum followed by 1 year compulsory clinical rotary internship",
            "Crack NEET-PG / INI-CET for advanced specialty residency (MD in Medicine or MS in Surgery)",
            "Pursue super-specialization (DM or M.Ch) for premier consultant stature"
        ]
    },
    {
        "id": "pharmacist_scientist",
        "title": "Pharmaceutical Research Scientist / Drug Developer",
        "stream": "medical",
        "level": "Graduation & Masters",
        "description": "Researches active chemical compounds, formulates life-saving medications, conducts clinical trials, and oversees pharmaceutical manufacturing standards.",
        "interests": "chemistry, biology, drugs, medicine making, pharmacy, drug discovery, clinical research, science, laboratory, health",
        "skills": "Organic Chemistry, Drug Formulation, HPLC Chromatography, Clinical Trial Analysis",
        "priorities": "impact, job stability, science, research, salary",
        "education": "B.Pharm (Bachelor of Pharmacy), M.Pharm, Pharm.D, Ph.D in Pharmaceutical Sciences",
        "colleges": [
            "Jamia Hamdard, New Delhi (NIRF #1 Pharmacy)",
            "BITS Pilani Department of Pharmacy",
            "NIPER (National Institute of Pharmaceutical Education & Research), Mohali",
            "Institute of Chemical Technology (ICT), Mumbai"
        ],
        "top_fields": [
            "Novel Drug Delivery Systems (NDDS) & Nanotechnology",
            "Pharmacology & Pharmacokinetics",
            "Regulatory Affairs & FDA Compliance",
            "Vaccine Formulation & Biologics"
        ],
        "companies": [
            "Sun Pharmaceutical Industries",
            "Dr. Reddy's Laboratories, Cipla",
            "Pfizer Global Research, Novartis, AstraZeneca",
            "Serum Institute of India, Biocon"
        ],
        "recommended_next_steps": [
            "Strengthen knowledge in Organic Chemistry, Biochemistry, and Human Physiology",
            "Take pharmacy entrance tests (State CETs, BITSAT, NEET)",
            "Gain practical laboratory experience in chemical synthesis and analytical instrumentation",
            "Target GPAT (Graduate Pharmacy Aptitude Test) for government-funded M.Pharm at NIPER",
            "Apply for R&D formulation or quality assurance scientist internships"
        ]
    },
    {
        "id": "corporate_lawyer",
        "title": "Corporate Lawyer & Legal Strategist",
        "stream": "humanities",
        "level": "Graduation",
        "description": "Negotiates high-stakes corporate contracts, guides cross-border mergers, safeguards intellectual property rights, and represents clients in judicial arbitrations.",
        "interests": "law, justice, debate, argumentation, court, advocacy, legal, reading, writing, rules, constitution, corporate deals, politics",
        "skills": "Contract Drafting, Legal Research, Cross-Examination, Negotiation, Statutory Interpretation",
        "priorities": "salary, prestige, high paying, intellectual challenge, authority",
        "education": "5-Year Integrated B.A. LLB / BBA LLB (Hons), LL.M",
        "colleges": [
            "NLSIU (National Law School of India University), Bengaluru",
            "NALSAR University of Law, Hyderabad",
            "The West Bengal National University of Juridical Sciences (WBNUJS), Kolkata",
            "National Law University (NLU), Delhi"
        ],
        "top_fields": [
            "Corporate Mergers & Acquisitions (M&A) Advisory",
            "Intellectual Property Rights (IPR, Patents & Trademarks)",
            "Tech, Artificial Intelligence & Data Privacy Law",
            "Commercial Arbitration & Supreme Court Litigation"
        ],
        "companies": [
            "Shardul Amarchand Mangaldas & Co (SAM)",
            "AZB & Partners, Cyril Amarchand Mangaldas (CAM)",
            "Khaitan & Co, Trilegal",
            "In-House Counsel at Google, Apple, Reliance Industries"
        ],
        "recommended_next_steps": [
            "Read legal precedents, constitutional landmarks, and business law developments daily",
            "Prepare for the CLAT (Common Law Admission Test) and AILET entrance exams",
            "Participate actively in Moot Court Competitions and Client Counseling tournaments",
            "Secure summer internships at Tier-1 law chambers and corporate legal departments",
            "Enrol with the Bar Council of India upon completing your law degree"
        ]
    },
    {
        "id": "ui_ux_product_designer",
        "title": "UI/UX & Digital Product Designer",
        "stream": "humanities",
        "level": "Graduation",
        "description": "Blends human psychology, visual aesthetics, typography, and interaction architecture to design seamless mobile applications, web experiences, and physical consumer products.",
        "interests": "design, art, creativity, visual, drawing, ui, ux, graphics, aesthetics, human psychology, sketching, colors, interfaces",
        "skills": "User Research, Wireframing, Figma, Design Systems, Usability Testing, Visual Prototyping",
        "priorities": "creativity, innovation, salary, high paying, work life balance",
        "education": "B.Des (Bachelor of Design) in Interaction / Industrial Design, B.Arch, M.Des",
        "colleges": [
            "NID (National Institute of Design), Ahmedabad",
            "IDC School of Design, IIT Bombay",
            "Department of Design, IIT Delhi & IIT Guwahati",
            "Srishti Manipal Institute of Art, Design & Technology, Bengaluru"
        ],
        "top_fields": [
            "User Experience (UX) Research & Behavioral Architecture",
            "User Interface (UI) Systems & Motion Design",
            "Consumer Product & Industrial Form Design",
            "AR/VR Spatial Computing & Game Experience Design"
        ],
        "companies": [
            "Apple Design Studio, Google Design",
            "Adobe, Microsoft Studio, Airbnb",
            "Zomato, Swiggy, CRED Product Teams",
            "Ogilvy, Pentagram, IDEO"
        ],
        "recommended_next_steps": [
            "Master design industry tools: Figma, Illustrator, and prototyping frameworks",
            "Study human-computer interaction (HCI) and cognitive design psychology principles",
            "Build a clean visual design portfolio showcasing 2 to 3 end-to-end case studies on Behance",
            "Prepare for UCEED, NID-DAT, and CEED design entrance examinations",
            "Redesign an existing product interface to demonstrate problem-solving intuition"
        ]
    },
    {
        "id": "civil_servant_upsc",
        "title": "Civil Services Officer (IAS / IPS / IFS)",
        "stream": "humanities",
        "level": "Graduation",
        "description": "Administers district governance, formulates national socio-economic policy, enforces law and order, and represents the sovereign nation in foreign diplomacy.",
        "interests": "civil services, upsc, ias, ips, government, administration, policy, society, public welfare, diplomacy, leadership, politics, change",
        "skills": "Public Policy Analysis, Administrative Decision Making, Crisis Leadership, Ethics, General Studies",
        "priorities": "impact, leadership, prestige, helping people, public authority, job stability",
        "education": "Graduation in any discipline (B.A. Political Science / History / Economics / B.Tech / MBBS)",
        "colleges": [
            "St. Stephen's College, University of Delhi",
            "Lady Shri Ram College (LSR), New Delhi",
            "Miranda House & Hindu College, Delhi",
            "Jawaharlal Nehru University (JNU), New Delhi"
        ],
        "top_fields": [
            "Indian Administrative Service (IAS - District & Ministerial Leadership)",
            "Indian Police Service (IPS - National Security & Law Enforcement)",
            "Indian Foreign Service (IFS - Global Diplomacy & Embassy Representation)",
            "Public Policy Formulation & NITI Aayog Advisory"
        ],
        "companies": [
            "Government of India (Union Public Service Commission - UPSC)",
            "State Governments (State Administrative Cadres)",
            "United Nations Development Programme (UNDP), World Bank Missions",
            "NITI Aayog & Think Tanks"
        ],
        "recommended_next_steps": [
            "Read national newspapers (The Hindu / Indian Express) and economic surveys analytically",
            "Pursue a rigorous bachelor's degree in Social Sciences or your chosen optional field",
            "Study standard foundational works in Indian Polity, History, Geography, and International Relations",
            "Practice answer-writing under time constraints for UPSC Mains descriptive papers",
            "Develop ethical reasoning, emotional intelligence, and interview communication skills"
        ]
    }
]

# Convert to Pandas DataFrame for efficient vectorization and queries
DF_CAREERS = pd.DataFrame(CAREERS_DATA)

# ---------------------------------------------------------------------------
# 2. NLP + TF-IDF Vectorization & Cosine Similarity ML Recommendation Engine
# ---------------------------------------------------------------------------
class CareerNLPEngine:
    """
    NLP & Machine Learning Recommendation Engine.
    Uses TF-IDF Vectorization to build numerical representations of student input
    and career profiles, then calculates Cosine Similarity scores to rank recommendations.
    """
    def __init__(self):
        # Create a rich semantic corpus string for each career
        self.career_corpus = []
        for idx, row in DF_CAREERS.iterrows():
            combined = f"{row['title']} {row['description']} {row['interests']} {row['skills']} {row['priorities']} {row['education']}"
            self.career_corpus.append(combined.lower())

        # Fit TF-IDF Vectorizer with n-grams (1, 2) to capture phrases like 'machine learning', 'high paying'
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.career_matrix = self.vectorizer.fit_transform(self.career_corpus)

    def extract_student_attributes(self, text: str) -> dict:
        """
        NLP Information Extraction Stage (Step 1):
        Identifies key interest domains, technical skills, and career priorities.
        """
        text_lower = text.lower()
        extracted = {
            "interests": [],
            "skills": [],
            "priorities": [],
            "summary_points": []
        }

        # Priority rules
        if any(w in text_lower for w in ["salary", "high-paying", "high paying", "money", "rich", "wealth", "earning"]):
            extracted["priorities"].append("High Earning Potential / Salary")
            extracted["summary_points"].append("You prioritize competitive earning potential and high compensation.")
        if any(w in text_lower for w in ["stability", "stable", "secure", "security"]):
            extracted["priorities"].append("Job Stability & Career Longevity")
            extracted["summary_points"].append("You value job security and organizational stability.")
        if any(w in text_lower for w in ["creativity", "creative", "art", "design", "visual", "aesthetic"]):
            extracted["priorities"].append("Creative Expression & Design Freedom")
            extracted["summary_points"].append("You are drawn to creative innovation and aesthetic design.")
        if any(w in text_lower for w in ["impact", "help", "helping", "society", "noble", "patient", "public"]):
            extracted["priorities"].append("Social Impact & Public Welfare")
            extracted["summary_points"].append("You want your work to directly benefit society and improve lives.")

        # Interest rules
        if any(w in text_lower for w in ["math", "mathematics", "calculus", "stats", "statistics", "numbers"]):
            extracted["interests"].append("Mathematics & Quantitative Modeling")
            extracted["summary_points"].append("You have strong enthusiasm for mathematics, numbers, and logic.")
        if any(w in text_lower for w in ["computer", "computers", "coding", "code", "programming", "software", "tech"]):
            extracted["interests"].append("Computers & Software Engineering")
            extracted["summary_points"].append("You enjoy computing technology and building software.")
        if any(w in text_lower for w in ["account", "accounting", "tax", "audit", "balance sheet", "finance", "stock"]):
            extracted["interests"].append("Finance, Accounts & Commercial Markets")
            extracted["summary_points"].append("You have a keen interest in finance, corporate accounts, and markets.")
        if any(w in text_lower for w in ["biology", "medicine", "doctor", "cure", "health", "hospital", "pharma"]):
            extracted["interests"].append("Medical, Life Sciences & Healthcare")
            extracted["summary_points"].append("You are fascinated by life sciences, medicine, and healthcare.")
        if any(w in text_lower for w in ["law", "debate", "justice", "court", "legal", "constitution", "argument"]):
            extracted["interests"].append("Law, Justice & Constitutional Advocacy")
            extracted["summary_points"].append("You are stimulated by legal argumentation, debate, and justice.")
        if any(w in text_lower for w in ["security", "hack", "hacking", "cyber", "defense", "investigat"]):
            extracted["interests"].append("Cyber Defense & Network Investigation")
            extracted["summary_points"].append("You are intrigued by cybersecurity, ethical hacking, and defense.")

        return extracted

    def recommend(self, student_profile_text: str, top_k: int = 3) -> list:
        """
        Step 2 & 3:
        1. Vectorizes student input text using TF-IDF.
        2. Calculates Cosine Similarity with all careers in database.
        3. Ranks and returns top_k recommendations with similarity scores and breakdown.
        """
        cleaned_text = student_profile_text.lower().strip()
        student_vec = self.vectorizer.transform([cleaned_text])

        # Cosine Similarity Calculation
        similarity_scores = cosine_similarity(student_vec, self.career_matrix)[0]

        # Get sorted indices in descending order
        top_indices = np.argsort(similarity_scores)[::-1][:top_k]

        recommendations = []
        for rank, idx in enumerate(top_indices, 1):
            score = float(similarity_scores[idx])
            career = CAREERS_DATA[idx]
            recommendations.append({
                "rank": rank,
                "score": round(score, 3),
                "score_percent": int(round(score * 100)),
                "career": career
            })

        return recommendations


# Initialize singleton instance of the ML engine
NLP_ENGINE = CareerNLPEngine()


# ---------------------------------------------------------------------------
# 3. Conversational State Manager (Chatbot Conversation Flow)
# ---------------------------------------------------------------------------
class ConversationalCareerBot:
    """
    Coordinates conversational dialogue, questions, and triggers the ML recommendation engine.
    Ensures a real multi-turn chatbot experience rather than a one-off form.
    """

    CONVERSATION_STAGES = [
        "stage_ask_subjects",
        "stage_ask_activities",
        "stage_ask_priority",
        "stage_completed"
    ]

    @classmethod
    def get_initial_greeting(cls):
        text = """### Welcome to Debris Careers AI 🏛️

I am your **NLP & Machine Learning Career Consultant**. 

Unlike simple keyword bots or generic LLMs, I use **Natural Language Processing (NLP)** and **TF-IDF Vectorization with Cosine Similarity** to mathematically match your unique interests, skills, and values against verified career trajectories.

---

#### Let's begin building your profile:
**What academic subjects or fields do you genuinely enjoy?**  
*(For example: "I like mathematics and computers", or "I enjoy biology and chemistry", or "I like accounts and economics")*
"""
        options = [
            "Mathematics & Computers",
            "Biology & Medicine",
            "Accounts & Economics",
            "Art, Design & Psychology",
            "Law, Debate & Politics"
        ]
        return text, {"stage": "stage_ask_subjects", "profile_answers": []}, options

    @classmethod
    def process_chat_message(cls, user_message: str, current_state: dict):
        """
        Handles user input through conversational stages or on-demand natural prompts.
        """
        text = user_message.strip()
        text_lower = text.lower()

        # Check for system navigation commands
        if text_lower in ["restart", "reset", "clear", "home", "start over"]:
            return cls.get_initial_greeting()

        if text_lower in ["help", "commands"]:
            help_text = """### Debris Careers — How to Use
- **Natural Profiling:** You can describe your interests in complete sentences:  
  *e.g. "I like mathematics, computers, and solving logical problems. I want a high-paying job."*
- **Conversational Guide:** Follow my step-by-step questions on your subjects, favourite activities, and career priorities.
- **Commands:** Type `restart` at any time to begin a fresh profile evaluation.
"""
            return help_text, current_state, ["Restart", "I like mathematics & computers", "I like accounts & finance"]

        # If user provides a comprehensive multi-intent prompt directly
        # (e.g. "I like mathematics, computers, and solving logical problems. I want a high-paying job.")
        word_count = len(text.split())
        extracted_info = NLP_ENGINE.extract_student_attributes(text)
        has_multiple_attributes = (len(extracted_info["interests"]) + len(extracted_info["priorities"])) >= 2

        if word_count >= 6 and has_multiple_attributes:
            return cls._generate_ml_recommendation_card(text, current_state)

        # Multi-turn Conversational Flow
        stage = current_state.get("stage", "stage_ask_subjects")
        profile_answers = current_state.get("profile_answers", [])

        if stage == "stage_ask_subjects":
            profile_answers.append(text)
            new_state = {
                "stage": "stage_ask_activities",
                "profile_answers": profile_answers
            }
            reply = f"""Got it! You enjoy **"{text}"**.

#### Question 2 of 3:
**What specific tasks or activities do you enjoy doing most?**  
*(For example: "Coding and building software", "Solving mathematical problems", "Managing accounts & balance sheets", "Designing visual layouts", or "Treating and helping patients")*
"""
            options = [
                "Coding & building software",
                "Solving complex logical & math problems",
                "Auditing accounts & financial analysis",
                "Creative UI/UX & visual sketching",
                "Debate, legal advocacy & justice",
                "Clinical patient care & biology research"
            ]
            return reply, new_state, options

        elif stage == "stage_ask_activities":
            profile_answers.append(text)
            new_state = {
                "stage": "stage_ask_priority",
                "profile_answers": profile_answers
            }
            reply = f"""Noted!

#### Final Question:
**What matters most to you in your future career?**  
• **Salary & Earning Potential** (High-paying corporate/tech growth)  
• **Job Stability & Security** (Reliable long-term career tenure)  
• **Creativity & Design Freedom** (Expressing original ideas)  
• **Social Impact & Public Good** (Helping people and society)
"""
            options = [
                "High Salary & Earning Potential",
                "Job Stability & Career Security",
                "Creativity & Innovation",
                "Social Impact & Helping People"
            ]
            return reply, new_state, options

        elif stage == "stage_ask_priority":
            profile_answers.append(text)
            combined_profile = " ".join(profile_answers)
            return cls._generate_ml_recommendation_card(combined_profile, current_state)

        else:
            # When completed or general query, run recommendation on current input
            return cls._generate_ml_recommendation_card(text, current_state)

    @classmethod
    def _generate_ml_recommendation_card(cls, full_student_text: str, state: dict):
        """
        Runs Step 1 through Step 5 of the ML Recommendation Pipeline.
        """
        # Step 1: NLP Extraction
        extracted = NLP_ENGINE.extract_student_attributes(full_student_text)
        
        # Step 2, 3, 4: TF-IDF Vectorization, Cosine Similarity, and Ranking
        top_recs = NLP_ENGINE.recommend(full_student_text, top_k=3)
        primary_match = top_recs[0]
        primary_career = primary_match["career"]

        # Step 5: Explain the Recommendation with Verified Templates
        summary_bullets = ""
        if extracted["summary_points"]:
            summary_bullets = "\n".join([f"  • {p}" for p in extracted["summary_points"]])
        else:
            summary_bullets = f"  • Matched keywords and contextual patterns in your response: *\"{full_student_text[:80]}...\"*"

        # Format Top 3 Ranking Table
        ranking_rows = []
        for r in top_recs:
            score_bar = "█" * int(r["score"] * 10) + "░" * (10 - int(r["score"] * 10))
            ranking_rows.append(f"| **#{r['rank']}** | **{r['career']['title']}** | `{r['score']}` ({r['score_percent']}%) | `{score_bar}` |")
        ranking_table = "\n".join(ranking_rows)

        # Format Next Steps
        steps_formatted = "\n".join([f"{i}. {step}" for i, step in enumerate(primary_career["recommended_next_steps"], 1)])
        colleges_formatted = "\n".join([f"  • {c}" for c in primary_career["colleges"]])
        fields_formatted = "\n".join([f"  • {f}" for f in primary_career["top_fields"]])
        companies_formatted = "\n".join([f"  • {cmp}" for cmp in primary_career["companies"]])

        reply = f"""### 🎯 NLP & Machine Learning Career Match Results

We analyzed your input profile through **TF-IDF Vectorization** and evaluated **Cosine Similarity** against our verified career database.

---

#### 📊 Ranked Career Matches (Cosine Similarity Scores):
| Rank | Recommended Career | Similarity Score | Confidence Match |
| :---: | :--- | :---: | :--- |
{ranking_table}

---

### 🏆 Top Recommended Match: **{primary_career['title']}**
*(Calculated Similarity Score: **{primary_match['score']}** / 1.00)*

> **Why this career matches your profile:**  
{summary_bullets}

**Academic Eligibility & Pathways:**  
{primary_career['education']}

---

#### 🏛️ Top Tier Colleges & Institutes:
{colleges_formatted}

#### 🎯 High-Demand Specializations:
{fields_formatted}

#### 🏢 Top Recruiting Companies & Organizations:
{companies_formatted}

---

#### 🚀 Recommended Next Action Steps:
{steps_formatted}
"""
        new_state = {
            "stage": "stage_completed",
            "last_recommendation": primary_career["id"],
            "profile_answers": [full_student_text]
        }
        
        options = [
            f"Explore #{top_recs[1]['rank']} ({top_recs[1]['career']['title'].split('/')[0].strip()})",
            f"Explore #{top_recs[2]['rank']} ({top_recs[2]['career']['title'].split('/')[0].strip()})",
            "Start Fresh Consultation",
            "What skills do I need?"
        ]
        return reply, new_state, options

    # Backward-compatible aliases for app.py
    @classmethod
    def get_welcome_response(cls):
        text, state, opts = cls.get_initial_greeting()
        return text, opts

    @classmethod
    def process_message(cls, user_message: str, current_state: dict):
        return cls.process_chat_message(user_message, current_state)


# For backward compatibility if imported elsewhere
CareerRuleEngine = ConversationalCareerBot
CAREER_KNOWLEDGE_BASE = {c["id"]: c for c in CAREERS_DATA}
