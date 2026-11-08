"""
Debris Careers - NLP + Machine Learning Career Recommendation Engine
Combines:
1. TF-IDF Vectorization & Cosine Similarity for personalized ML recommendation.
2. Rule-based structured knowledge retrieval (Colleges, Courses, Hiring Companies, Next Steps).
3. Conversational AI Consultant (Pure natural input -> Intelligent relevant answer, Zero forced MCQs).
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
        "interests": "mathematics, computers, machine learning, artificial intelligence, statistics, algorithms, logical reasoning, data analysis, deep learning, prediction, ai, quant",
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
        "entrance_exams": "JEE Main, JEE Advanced, ISI Admission Test, GATE",
        "recommended_next_steps": [
            "Master Python and essential data libraries (NumPy, Pandas, Scikit-Learn)",
            "Build strong foundations in Linear Algebra, Probability, and Multivariate Calculus",
            "Learn SQL and database querying for large real-world datasets",
            "Create end-to-end data analysis and machine learning portfolio projects on Kaggle or GitHub",
            "Target entrance tests (JEE Main/Advanced, ISI Admission Test) for top institutions"
        ]
    },
    {
        "id": "software_engineer",
        "title": "Software Development Engineer (SDE / Systems Architect)",
        "stream": "non_medical",
        "level": "Graduation",
        "description": "Designs, develops, tests, and architects scalable software systems, web applications, cloud infrastructure, and low-latency distributed systems.",
        "interests": "coding, computers, software, web development, app development, algorithms, system design, problem solving, technology, building products, programming, computer science, cse",
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
        "entrance_exams": "JEE Main, JEE Advanced, BITSAT",
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
        "interests": "computers, security, ethical hacking, cyber defense, investigation, cryptography, forensics, network defense, curiosity, cyber, hacker",
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
        "entrance_exams": "JEE Main, State CETs",
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
        "interests": "accounts, accounting, mathematics, balance sheet, tax, taxation, auditing, audit, finance, corporate law, business numbers, precision, ca, gst",
        "skills": "Auditing, Financial Accounting, GST/Direct Taxation, Financial Modeling, Analytical Precision",
        "priorities": "salary, prestige, high paying, job stability, corporate authority",
        "education": "ICAI Qualification (Foundation, Inter, Articleship, Final) concurrently with B.Com (Hons)",
        "colleges": [
            "Institute of Chartered Accountants of India (ICAI - Governing Body)",
            "SRCC (Shri Ram College of Commerce), Delhi University",
            "Loyola College, Chennai",
            "St. Xavier's College, Kolkata / Mumbai",
            "Hansraj College & Hindu College, Delhi"
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
        "entrance_exams": "CA Foundation, CUET-UG (for top Commerce colleges)",
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
        "interests": "finance, stock market, investment, trading, equity, wall street, banking, valuation, mergers, acquisitions, economy, money, business, financial markets",
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
        "entrance_exams": "CUET-UG, CAT, GMAT, CFA Program",
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
        "interests": "biology, human body, medicine, doctor, cure, disease, surgery, healing, hospital, patient, healthcare, science, empathy, mbbs, clinical",
        "skills": "Clinical Diagnosis, Surgical Precision, Emergency Care, Pharmacology, Empathy",
        "priorities": "impact, helping people, job stability, prestige, salary, noble profession",
        "education": "MBBS (Bachelor of Medicine & Surgery) + MD/MS / DM/M.Ch Super-specialization",
        "colleges": [
            "AIIMS (All India Institute of Medical Sciences), New Delhi",
            "Christian Medical College (CMC), Vellore",
            "Armed Forces Medical College (AFMC), Pune",
            "JIPMER Puducherry & KGMU Lucknow",
            "Kasturba Medical College (KMC), Manipal"
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
        "entrance_exams": "NEET-UG, NEET-PG / INI-CET",
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
        "interests": "chemistry, biology, drugs, medicine making, pharmacy, drug discovery, clinical research, science, laboratory, health, b.pharm",
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
        "entrance_exams": "State CETs, BITSAT, GPAT",
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
        "interests": "law, justice, debate, argumentation, court, advocacy, legal, reading, writing, rules, constitution, corporate deals, politics, lawyer, judiciary",
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
        "entrance_exams": "CLAT (Common Law Admission Test), AILET",
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
        "interests": "design, art, creativity, visual, drawing, ui, ux, graphics, aesthetics, human psychology, sketching, colors, interfaces, product design, animation",
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
        "entrance_exams": "UCEED, NID-DAT, NIFT Entrance",
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
        "interests": "civil services, upsc, ias, ips, government, administration, policy, society, public welfare, diplomacy, leadership, politics, change, district collector",
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
        "entrance_exams": "UPSC Civil Services Examination (Prelims, Mains, Interview)",
        "recommended_next_steps": [
            "Read national newspapers (The Hindu / Indian Express) and economic surveys analytically",
            "Pursue a rigorous bachelor's degree in Social Sciences or your chosen optional field",
            "Study standard foundational works in Indian Polity, History, Geography, and International Relations",
            "Practice answer-writing under time constraints for UPSC Mains descriptive papers",
            "Develop ethical reasoning, emotional intelligence, and interview communication skills"
        ]
    }
]

DF_CAREERS = pd.DataFrame(CAREERS_DATA)

# ---------------------------------------------------------------------------
# 2. NLP + TF-IDF Vectorization & Cosine Similarity ML Engine
# ---------------------------------------------------------------------------
class CareerNLPEngine:
    def __init__(self):
        self.career_corpus = []
        for idx, row in DF_CAREERS.iterrows():
            combined = f"{row['title']} {row['description']} {row['interests']} {row['skills']} {row['priorities']} {row['education']}"
            self.career_corpus.append(combined.lower())

        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.career_matrix = self.vectorizer.fit_transform(self.career_corpus)

    def extract_student_attributes(self, text: str) -> dict:
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
        if any(w in text_lower for w in ["computer", "computers", "coding", "code", "programming", "software", "tech", "sde", "developer"]):
            extracted["interests"].append("Computers & Software Engineering")
            extracted["summary_points"].append("You enjoy computing technology and building software.")
        if any(w in text_lower for w in ["account", "accounting", "tax", "audit", "balance sheet", "finance", "stock", "ca", "gst"]):
            extracted["interests"].append("Finance, Accounts & Commercial Markets")
            extracted["summary_points"].append("You have a keen interest in finance, corporate accounts, and markets.")
        if any(w in text_lower for w in ["biology", "medicine", "doctor", "cure", "health", "hospital", "pharma", "mbbs"]):
            extracted["interests"].append("Medical, Life Sciences & Healthcare")
            extracted["summary_points"].append("You are fascinated by life sciences, medicine, and healthcare.")
        if any(w in text_lower for w in ["law", "debate", "justice", "court", "legal", "constitution", "argument", "lawyer"]):
            extracted["interests"].append("Law, Justice & Constitutional Advocacy")
            extracted["summary_points"].append("You are stimulated by legal argumentation, debate, and justice.")
        if any(w in text_lower for w in ["security", "hack", "hacking", "cyber", "defense", "investigat"]):
            extracted["interests"].append("Cyber Defense & Network Investigation")
            extracted["summary_points"].append("You are intrigued by cybersecurity, ethical hacking, and defense.")
        if any(w in text_lower for w in ["design", "ui", "ux", "graphics", "product design"]):
            extracted["interests"].append("UI/UX & Product Design")
            extracted["summary_points"].append("You are excited by digital interfaces, aesthetics, and user experience.")
        if any(w in text_lower for w in ["upsc", "ias", "ips", "civil services", "government"]):
            extracted["interests"].append("Public Administration & Civil Services")
            extracted["summary_points"].append("You are aiming for public leadership and administrative service.")

        return extracted

    def recommend(self, student_profile_text: str, top_k: int = 3) -> list:
        cleaned_text = student_profile_text.lower().strip()
        student_vec = self.vectorizer.transform([cleaned_text])

        similarity_scores = cosine_similarity(student_vec, self.career_matrix)[0]
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


NLP_ENGINE = CareerNLPEngine()


# ---------------------------------------------------------------------------
# 3. Conversational AI Career Consultant (No MCQs, Pure Input-driven advisory)
# ---------------------------------------------------------------------------
class ConversationalCareerBot:
    """
    Intelligent Career Consultant:
    - Waits for the student's input.
    - Evaluates natural queries, interest descriptions, specific questions, or stream inquiries.
    - Delivers deeply relevant, structured answers (Colleges, Courses, Recruiters, Next Steps).
    - NEVER forces multiple choice questions or quiz stages!
    """

    @classmethod
    def get_welcome_response(cls):
        """
        Initial greeting for empty state.
        Options list is empty - no MCQ buttons!
        """
        text = """### Welcome to Debris Careers AI 🏛️

I am your **AI & NLP Career Consultant**. 

Tell me about your **favourite subjects, skills, interests, or career ambitions** in your own words, and I'll analyze the optimal career trajectories, premier colleges, and top hiring companies for you.

*(For example: "I am interested in accounts and finance", or "I like coding, math, and want a high-paying job", or "Tell me about law colleges and careers")*
"""
        return text, []

    @classmethod
    def process_chat_message(cls, user_message: str, current_state: dict):
        text = user_message.strip()
        text_lower = text.lower()

        if not text:
            return "Please type a subject, skill, or career question you would like to explore.", current_state, []

        # 1. System Navigation Commands
        if text_lower in ["restart", "reset", "clear", "home", "start over"]:
            welcome_text, _ = cls.get_welcome_response()
            return welcome_text, {}, []

        if text_lower in ["help", "commands"]:
            help_text = """### Debris Careers AI — Guide
You can ask me anything about careers, academic streams, degrees, colleges, and jobs:
- **Describe your profile:** *"I like mathematics, computers, and solving logical problems. I want a high-paying job."*
- **Explore a specific field:** *"I am interested in accounts"*, *"Tell me about UI/UX design"*, *"How to become a doctor?"*
- **Ask specific questions:** *"Which colleges are best for B.Tech CSE?"*, *"What entrance exams are needed for law?"*, *"Top recruiters for data scientists?"*
"""
            return help_text, current_state, []

        # 2. Greetings
        if text_lower in ["hello", "hi", "hey", "good morning", "good evening", "greetings"]:
            reply = """### Hello! Welcome to Debris Careers 👋

I'm your AI consultant. I'm ready whenever you are! 

Tell me about your **interests, subjects you enjoy, or questions about any career field**, and I'll give you a detailed breakdown of degrees, top colleges, and recruiting companies.
"""
            return reply, current_state, []

        # 3. Direct domain / keyword search
        direct_career = cls._match_direct_career_intent(text_lower)
        if direct_career:
            reply = cls._format_single_career_card(direct_career, user_query=text)
            return reply, {"last_career": direct_career["id"]}, []

        # 4. Stream-level guidance
        stream_reply = cls._check_stream_guidance(text_lower)
        if stream_reply:
            return stream_reply, current_state, []

        # 5. Specific question handling (e.g., colleges, skills, salary, entrance exams)
        specific_answer = cls._answer_targeted_question(text_lower, current_state)
        if specific_answer:
            return specific_answer, current_state, []

        # 6. Natural multi-attribute profile scoring via TF-IDF & Cosine Similarity
        reply = cls._generate_ml_recommendation_card(text, current_state)
        return reply, {"last_query": text}, []

    @classmethod
    def _match_direct_career_intent(cls, text_lower: str):
        """Matches direct field intent (e.g. 'accounts', 'coding', 'doctor', 'law', etc.)."""
        # Keyword mappings to career ids
        mappings = [
            (["account", "accounts", "accounting", "ca", "chartered accountant", "auditing", "taxation", "balance sheet", "gst"], "chartered_accountant"),
            (["data scientist", "data science", "machine learning", "ai engineer", "artificial intelligence", "predictive model"], "data_scientist"),
            (["software", "developer", "coding", "programmer", "programming", "web dev", "app dev", "sde", "computer science"], "software_engineer"),
            (["cybersecurity", "cyber", "ethical hacking", "hacker", "network security", "infosec", "penetration testing"], "cybersecurity_analyst"),
            (["investment bank", "investment banking", "equity research", "stock market", "wall street", "portfolio manager", "trading"], "investment_banker"),
            (["doctor", "mbbs", "medicine", "surgeon", "physician", "clinical", "hospital", "patient care"], "medical_physician"),
            (["pharmacy", "pharmacist", "drug discovery", "pharmaceutical", "b.pharm", "medicine making"], "pharmacist_scientist"),
            (["law", "lawyer", "advocate", "judge", "judiciary", "legal", "court", "llb", "nlu"], "corporate_lawyer"),
            (["ui", "ux", "ui/ux", "product design", "designer", "graphic design", "figma", "visual design"], "ui_ux_product_designer"),
            (["upsc", "ias", "ips", "civil services", "district collector", "diplomat", "ifs", "civil servant"], "civil_servant_upsc")
        ]

        for keywords, career_id in mappings:
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    for c in CAREERS_DATA:
                        if c["id"] == career_id:
                            return c
        return None

    @classmethod
    def _check_stream_guidance(cls, text_lower: str):
        """Checks if student is asking for high-level stream overview."""
        if any(k in text_lower for k in ["non-medical", "non medical", "engineering stream", "stem"]):
            return """### Non-Medical & Engineering Pathways ⚙️

Driven by mathematics, computing, and physical sciences. Here are the premier avenues:

1. **Computer Science & Artificial Intelligence (B.Tech CSE/AI):**  
   Software Engineering, Distributed Systems, Data Science, and Machine Learning.
   *Colleges:* IIT Bombay, IIT Delhi, BITS Pilani, IIIT Hyderabad.  
   *Recruiters:* Google, Microsoft, NVIDIA, Amazon.

2. **Electronics & Communication (ECE / VLSI):**  
   Semiconductor chip design, robotics, and embedded systems.
   *Colleges:* IIT Kharagpur, BITS Pilani, NIT Warangal.  
   *Recruiters:* Qualcomm, Intel, Texas Instruments.

3. **Data Science & Quantitative Mathematics (B.Sc / ISI):**  
   Algorithmic trading, statistical modeling, and quantitative analytics.
   *Colleges:* ISI Kolkata, CMI, IISc Bangalore.  
   *Recruiters:* WorldQuant, Tower Research, Goldman Sachs.

*Tell me what specific domain or subjects inside Non-Medical you enjoy, and I'll give you a tailored plan!*
"""

        if any(k in text_lower for k in ["medical stream", "biology stream", "medical options", "after 12th medical"]):
            return """### Medical & Healthcare Sciences Pathways 🩺

Dedicated to life sciences, clinical care, pharmaceuticals, and healing. Core avenues:

1. **Clinical Medicine & Surgery (MBBS & MD/MS):**  
   The premier route to becoming a physician, surgeon, or clinical specialist.  
   *Colleges:* AIIMS New Delhi, CMC Vellore, JIPMER, KMC Manipal.  
   *Recruiters:* Apollo Hospitals, Max Super Speciality, Fortis Healthcare.

2. **Pharmaceutical Sciences (B.Pharm & M.Pharm):**  
   Drug discovery, clinical trials, formulation, and quality assurance.  
   *Colleges:* Jamia Hamdard, BITS Pilani, NIPER Mohali, ICT Mumbai.  
   *Recruiters:* Sun Pharma, Dr. Reddy's, Pfizer, Cipla.

3. **Biotechnology & Biomedical Research (B.Sc / B.Tech Biotech):**  
   Genetic engineering, CRISPR vaccine development, and bioinformatics.  
   *Colleges:* St. Xavier's, Loyola College, IISc Bangalore.  
   *Recruiters:* Biocon, Syngene, Bharat Biotech.

*Are you leaning towards clinical patient care or pharmaceutical research? Let me know!*
"""

        if any(k in text_lower for k in ["commerce stream", "business stream", "after 12th commerce"]):
            return """### Commerce, Finance & Business Management Pathways 📈

The backbone of capital markets, corporate balance sheets, and enterprise growth:

1. **Chartered Accountancy (CA) & B.Com (Hons):**  
   Statutory auditing, taxation, corporate financial restructuring, and CFO advisory.  
   *Colleges:* ICAI + SRCC, LSR, Loyola College, St. Xavier's.  
   *Recruiters:* Big 4 (Deloitte, PwC, EY, KPMG), BDO, Reliance, Tata Sons.

2. **Investment Banking & Equity Markets (CFA / MBA Finance):**  
   M&A advisory, IPOs, valuation, and capital allocation.  
   *Colleges:* IIM Ahmedabad, IIM Bangalore, FMS Delhi.  
   *Recruiters:* Goldman Sachs, Morgan Stanley, JP Morgan Chase.

3. **Business Management (BBA / BMS / IPM):**  
   Corporate strategy, brand management, operations, and leadership.  
   *Colleges:* SSCBS Delhi, IIM Indore (IPM), NMIMS Mumbai.  
   *Recruiters:* McKinsey, Bain & Company, HUL, P&G.

*Tell me if you prefer accounting & auditing, stock markets & investment, or general business management!*
"""

        if any(k in text_lower for k in ["humanities", "arts stream", "after 12th arts"]):
            return """### Humanities, Social Sciences, Law & Design Pathways ⚖️

Focuses on human society, justice, public governance, creative expression, and media:

1. **Corporate Law & Litigation (5-Year Integrated B.A. LLB):**  
   Corporate M&A, intellectual property, constitutional litigation, and arbitration.  
   *Colleges:* NLSIU Bengaluru, NALSAR Hyderabad, NLU Delhi.  
   *Recruiters:* Shardul Amarchand, AZB & Partners, Google Legal, Trilegal.

2. **UI/UX & Product Design (B.Des):**  
   Interface design, visual design systems, and consumer product architecture.  
   *Colleges:* NID Ahmedabad, IDC IIT Bombay, NIFT New Delhi.  
   *Recruiters:* Apple, Google Design, Adobe, Swiggy, Zomato.

3. **Civil Services & Public Governance (UPSC CSE):**  
   District administration, national policy formulation, and diplomacy (IAS / IPS / IFS).  
   *Colleges:* St. Stephen's, LSR, Miranda House, JNU.  
   *Recruiters:* Government of India, State Governments, United Nations.

*Which of these areas sparks your passion most? Tell me more!*
"""
        return None

    @classmethod
    def _answer_targeted_question(cls, text_lower: str, state: dict):
        """Answers targeted questions about colleges, skills, salary, or exams for a previously mentioned or current career."""
        # Find which career is relevant
        target_career = None
        for c in CAREERS_DATA:
            if c["id"] in text_lower or any(kw in text_lower for kw in c["title"].lower().split("/")):
                target_career = c
                break

        if not target_career and state.get("last_career"):
            for c in CAREERS_DATA:
                if c["id"] == state["last_career"]:
                    target_career = c
                    break

        if not target_career:
            return None

        # Check question type
        if any(q in text_lower for q in ["college", "colleges", "university", "institutes", "where to study"]):
            colleges_md = "\n".join([f"  • **{col}**" for col in target_career["colleges"]])
            return f"""### 🏛️ Premier Colleges for {target_career['title']}

Here are the highest-ranked institutions known for faculty, research facilities, and campus recruitment in this domain:

{colleges_md}

**Primary Entrance Benchmark:** {target_career.get('entrance_exams', 'National / University Entrance Tests')}  
**Recommended Degree:** {target_career['education']}
"""

        if any(q in text_lower for q in ["skill", "skills", "what do i need to learn", "requirements"]):
            steps_md = "\n".join([f"{i}. {step}" for i, step in enumerate(target_career["recommended_next_steps"], 1)])
            return f"""### 🎯 Key Skills & Learning Roadmap for {target_career['title']}

**Core Technical & Professional Skills:**  
`{target_career['skills']}`

**Recommended Sequential Next Steps:**  
{steps_md}
"""

        if any(q in text_lower for q in ["company", "companies", "recruiters", "who hires", "jobs"]):
            companies_md = "\n".join([f"  • **{cmp}**" for cmp in target_career["companies"]])
            fields_md = "\n".join([f"  • {f}" for f in target_career["top_fields"]])
            return f"""### 🏢 Top Recruiters & Career Roles for {target_career['title']}

**Active Hiring Organizations:**  
{companies_md}

**High-Demand Specializations & Target Job Profiles:**  
{fields_md}
"""

        if any(q in text_lower for q in ["exam", "entrance", "admission"]):
            return f"""### 📝 Admission & Entrance Exams for {target_career['title']}

**Benchmark Entrance Examinations:**  
`{target_career.get('entrance_exams', 'National & State Level Admissions')}`

**Target Degree Pathway:**  
{target_career['education']}

*Make sure to prepare syllabus fundamentals and track official application windows early!*
"""

        return None

    @classmethod
    def _format_single_career_card(cls, career: dict, user_query: str = ""):
        """Renders a comprehensive, clean, professional advisory card for a specific career."""
        colleges_md = "\n".join([f"  • {c}" for c in career["colleges"]])
        fields_md = "\n".join([f"  • {f}" for f in career["top_fields"]])
        companies_md = "\n".join([f"  • {cmp}" for cmp in career["companies"]])
        steps_md = "\n".join([f"{i}. {step}" for i, step in enumerate(career["recommended_next_steps"], 1)])

        card = f"""### Career Advisory: {career['title']}

> {career['description']}

---

#### 🎓 Recommended Degree & Pathways:
**{career['education']}**  
*(Entrance Benchmark: {career.get('entrance_exams', 'National Admissions')})*

#### 🏛️ Top Tier Colleges & Institutes:
{colleges_md}

#### 🎯 High-Demand Specializations & Skills:
{fields_md}  
*Key Skills:* `{career['skills']}`

#### 🏢 Top Recruiting Companies & Organizations:
{companies_md}

---

#### 🚀 Recommended Actionable Next Steps:
{steps_md}
"""
        return card

    @classmethod
    def _generate_ml_recommendation_card(cls, full_student_text: str, state: dict):
        """
        Runs NLP extraction + TF-IDF Vectorization & Cosine Similarity ranking.
        """
        extracted = NLP_ENGINE.extract_student_attributes(full_student_text)
        top_recs = NLP_ENGINE.recommend(full_student_text, top_k=3)
        primary_match = top_recs[0]
        primary_career = primary_match["career"]

        summary_bullets = ""
        if extracted["summary_points"]:
            summary_bullets = "\n".join([f"  • {p}" for p in extracted["summary_points"]])
        else:
            summary_bullets = f"  • Analyzed keywords and domain context from your query: *\"{full_student_text[:80]}...\"*"

        ranking_rows = []
        for r in top_recs:
            score_bar = "█" * int(r["score"] * 10) + "░" * (10 - int(r["score"] * 10))
            ranking_rows.append(f"| **#{r['rank']}** | **{r['career']['title']}** | `{r['score']}` ({r['score_percent']}%) | `{score_bar}` |")
        ranking_table = "\n".join(ranking_rows)

        steps_formatted = "\n".join([f"{i}. {step}" for i, step in enumerate(primary_career["recommended_next_steps"], 1)])
        colleges_formatted = "\n".join([f"  • {c}" for c in primary_career["colleges"]])
        fields_formatted = "\n".join([f"  • {f}" for f in primary_career["top_fields"]])
        companies_formatted = "\n".join([f"  • {cmp}" for cmp in primary_career["companies"]])

        reply = f"""### 🎯 Career Match Analysis (NLP & Machine Learning)

We analyzed your query through **TF-IDF Vectorization** and calculated **Cosine Similarity** against our verified institutional database.

---

#### 📊 Ranked Career Matches:
| Rank | Recommended Career | Similarity Score | Match Level |
| :---: | :--- | :---: | :--- |
{ranking_table}

---

### 🏆 Top Recommended Match: **{primary_career['title']}**
*(Similarity Score: **{primary_match['score']}** / 1.00)*

> **Why this career matches your input:**  
{summary_bullets}

**Academic Eligibility & Pathways:**  
{primary_career['education']}  
*(Entrance Benchmark: {primary_career.get('entrance_exams', 'National Tests')})*

---

#### 🏛️ Top Tier Colleges & Institutes:
{colleges_formatted}

#### 🎯 High-Demand Specializations & Skills:
{fields_formatted}  
*Key Skills:* `{primary_career['skills']}`

#### 🏢 Top Recruiting Companies & Organizations:
{companies_formatted}

---

#### 🚀 Recommended Actionable Next Steps:
{steps_formatted}
"""
        return reply

    # Backward-compatible method
    @classmethod
    def process_message(cls, user_message: str, current_state: dict):
        return cls.process_chat_message(user_message, current_state)


CareerRuleEngine = ConversationalCareerBot
CAREER_KNOWLEDGE_BASE = {c["id"]: c for c in CAREERS_DATA}
