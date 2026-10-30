"""
Debris Careers - College Project Report & Viva Guide Generator
Generates a comprehensive multi-page PDF document for professors, evaluators, and viva defense.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import textwrap

PDF_PATH = "/Users/sarthksn/.gemini/antigravity/scratch/debris-careers/Debris_Careers_Project_Report_Viva_Guide.pdf"

PAGES_DATA = [
    {
        "title": "DEBRIS CAREERS — PROJECT REPORT & VIVA GUIDE",
        "subtitle": "AI, Natural Language Processing (NLP) & Decision-Tree Career Consultant",
        "sections": [
            ("1. PROJECT METADATA & EXECUTIVE SUMMARY", [
                "• Project Name: Debris Careers",
                "• Domain: Artificial Intelligence, Natural Language Processing (NLP) & Information Retrieval (IR)",
                "• Purpose: A deterministic, personalized career consulting platform designed for college students and graduates.",
                "• Core Philosophy: Zero hallucination, zero paid API dependency, 100% offline local machine learning.",
                "• Key Technology Stack: Python 3, Flask, scikit-learn (TF-IDF & Cosine Similarity), Pandas, SQLite3, HTML5/CSS3.",
                "• Visual Architecture: Minimalist Monochrome Liquid Glass (Glassmorphism), Porsche Typography, Dynamic Themes."
            ]),
            ("2. MOTIVATION & PROBLEM STATEMENT", [
                "• Career confusion is a major challenge for school and university students facing rapid industry transformations.",
                "• Traditional web forms are rigid, passive, and fail to provide personalized or explainable guidance.",
                "• Generative AI / LLM chatbots often hallucinate non-existent degrees, fabricate university details, or cost money via APIs.",
                "• Solution: Debris Careers pairs a stateful multi-turn conversational interface with a mathematical TF-IDF",
                "  vectorization engine to deliver reliable, explainable recommendations backed by verified institutional data."
            ]),
            ("3. ARCHITECTURAL OVERVIEW", [
                "• Tier 1 (Presentation): Soothing Liquid-Glass web interface with ambient harmonic particles and Light/Dark themes.",
                "• Tier 2 (Application Server): Lightweight Flask controller managing sessions, chat routes, and database operations.",
                "• Tier 3 (Inference Engine): Dual-mode system featuring direct NLP attribute extraction and a multi-turn profiler.",
                "• Tier 4 (Data & Persistence): Relational SQLite3 database storing users, consultations, and message history."
            ])
        ]
    },
    {
        "title": "MACHINE LEARNING & NLP RECOMMENDATION PIPELINE",
        "subtitle": "5-Stage Mathematical Pipeline for Deterministic Recommendations",
        "sections": [
            ("STAGE 1: NLP ATTRIBUTE EXTRACTION", [
                "• When a student inputs a natural statement (e.g., 'I like mathematics and computers. I want a high-paying job'):",
                "• The text is normalized, tokenized, and evaluated across semantic lexicons (Interests, Skills, Career Values).",
                "• Extracts explicit priorities: High Salary, Job Stability, Creative Freedom, or Social Impact."
            ]),
            ("STAGE 2: TF-IDF VECTORIZATION (TERM FREQUENCY - INVERSE DOCUMENT FREQUENCY)", [
                "• Machine learning models operate on numerical representations rather than raw strings.",
                "• Uses scikit-learn's TfidfVectorizer with sublinear term-frequency scaling and unigram + bigram (1, 2) ranges.",
                "• Formula: TF-IDF(t, d, D) = TF(t, d) * IDF(t, D), where IDF(t, D) = ln((1 + |D|) / (1 + DF(t, D))) + 1.",
                "• Converts student input and all pre-curated career profiles into high-dimensional numerical feature vectors."
            ]),
            ("STAGE 3: COSINE SIMILARITY CALCULATION", [
                "• Computes the mathematical angle between the student's vector (S) and each career feature vector (C):",
                "• Formula: Cosine_Similarity(S, C) = (S • C) / (||S|| * ||C||) = Sum(S_i * C_i) / (Sqrt(Sum(S_i^2)) * Sqrt(Sum(C_i^2))).",
                "• Yields a normalized relevance score between 0.00 and 1.00 (displayed as a percentage confidence bar)."
            ]),
            ("STAGE 4 & 5: RANKING & VERIFIED EXPLANATION SYNTHESIS", [
                "• Sorts cosine similarity scores in descending order and selects the Top 3 best matches.",
                "• Explains WHY the match occurred based on extracted keywords, avoiding opaque black-box outputs.",
                "• Delivers: Required Degrees, Top Tier Colleges (IITs, AIIMS, SRCC, NLSIU), Top Recruiters, and a 5-Step Action Plan."
            ])
        ]
    },
    {
        "title": "CONVERSATIONAL FLOW & DATABASE SECURITY",
        "subtitle": "Multi-Turn Dialogue Management & Relational SQLite Architecture",
        "sections": [
            ("MULTI-TURN CHATBOT VS. STATIC FORMS", [
                "• Unlike a one-off form, Debris Careers conducts an interactive, multi-turn consultation:",
                "  - Turn 1: Academic subjects and foundational interests (e.g., Math, Bio, Accounts, Law).",
                "  - Turn 2: Day-to-day functional activities (e.g., Coding, Clinical Diagnosis, Auditing, Visual Design).",
                "  - Turn 3: Core career drivers and priorities (e.g., High Salary, Stability, Creativity, Social Impact).",
                "• Flexible Execution: Users can also input a complete natural prompt at any time to trigger instant scoring."
            ]),
            ("DATABASE SCHEMA & PERSISTENCE (SQLite3)", [
                "• Table 1: users (id, email UNIQUE, password_hash, created_at)",
                "• Table 2: conversations (id UUID PRIMARY KEY, user_id FK, title, state_data JSON, created_at, updated_at)",
                "• Table 3: messages (id, conversation_id FK, sender ['user'/'bot'], content, options JSON, timestamp)",
                "• Full Session Retention: Chat histories persist across logins, with options to delete individual chats or clear all."
            ]),
            ("SECURITY CONSTRAINTS & PASSWORD POLICY", [
                "• Explicit Constraint: Maximum password length of 8 characters.",
                "• Dual-Layer Enforcement: Enforced at both presentation (HTML maxlength='8') and server (Python len <= 8) layers.",
                "• Cryptographic Hashing: Passwords are salted and hashed using SHA-256 before database insertion."
            ])
        ]
    },
    {
        "title": "AESTHETICS, UI INNOVATIONS & VIVA CHEATSHEET",
        "subtitle": "Design Psychology & Comprehensive Q&A for Evaluators",
        "sections": [
            ("SOOTHING VISUAL AESTHETICS (GLASSMORPHISM & BEIGE PALETTE)", [
                "• Design Purpose: Reduces career planning anxiety and cognitive fatigue.",
                "• Warm Frosted Beige Palette: Warm cream (#FAF6F0) and oat canvas with frosted liquid-glass panels.",
                "• Porsche Headline Typography: Exclusive '911 Porscha' headline typography paired with modern sans-serif body text.",
                "• Ambient Constellation Canvas: HTML5 canvas displaying 60-75 gently floating particles in harmonic sine-wave orbits.",
                "• Dynamic Theme Toggle: Instant transition between soothing Warm Beige and deep Cosmic Obsidian Dark Mode."
            ]),
            ("COLLEGE VIVA CHEATSHEET — HIGH-YIELD QUESTIONS & ANSWERS", [
                "Q1: Why use TF-IDF and Cosine Similarity instead of OpenAI / ChatGPT API?",
                "Ans: LLMs are prone to hallucinations, require paid API keys, and have network latency. Our approach runs 100% offline,",
                "     produces explainable mathematical similarity scores, and guarantees accurate college and recruiter information.",
                "",
                "Q2: How does the chatbot recognize keywords without an LLM?",
                "Ans: We use a dual-tier NLP architecture: Step 1 extracts semantic entities (subjects, priorities); Step 2 calculates",
                "     cosine similarity across n-gram vector spaces, mapping student intent to verified career profiles.",
                "",
                "Q3: How are career recommendations explained to students?",
                "Ans: Rather than generating text probabilistically, the system synthesizes verified templates detailing matching traits,",
                "     academic pathways, top colleges (e.g., IITs, SRCC, AIIMS), top recruiters (e.g., Google, Deloitte), and next steps."
            ])
        ]
    }
]

def generate_pdf():
    pdf = PdfPages(PDF_PATH)
    
    for page_idx, page in enumerate(PAGES_DATA):
        # Create standard Letter portrait page (8.5 x 11 inches)
        fig = plt.figure(figsize=(8.5, 11), facecolor='#FAF7F2')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        # Outer decorative double border
        rect1 = plt.Rectangle((0.03, 0.03), 0.94, 0.94, fill=False, edgecolor='#B4A08C', linewidth=1.2, transform=ax.transAxes)
        rect2 = plt.Rectangle((0.035, 0.035), 0.93, 0.93, fill=False, edgecolor='#DCD0C0', linewidth=0.6, transform=ax.transAxes)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        
        # Header banner
        header_box = plt.Rectangle((0.05, 0.88), 0.90, 0.075, facecolor='#1C1917', edgecolor='#1C1917', transform=ax.transAxes)
        ax.add_patch(header_box)
        
        # Header text
        ax.text(0.50, 0.925, page["title"], color='#FAF6F0', fontsize=12, fontweight='bold', ha='center', va='center', transform=ax.transAxes)
        ax.text(0.50, 0.895, page["subtitle"], color='#DCD0C0', fontsize=8.5, fontstyle='italic', ha='center', va='center', transform=ax.transAxes)
        
        # Content positioning
        y_cursor = 0.84
        for sec_title, items in page["sections"]:
            # Section header bar
            sec_bg = plt.Rectangle((0.05, y_cursor - 0.022), 0.90, 0.026, facecolor='#EDE4D8', edgecolor='#D0C4B4', linewidth=0.8, transform=ax.transAxes)
            ax.add_patch(sec_bg)
            ax.text(0.065, y_cursor - 0.009, sec_title, color='#1C1917', fontsize=9.5, fontweight='bold', va='center', transform=ax.transAxes)
            y_cursor -= 0.038
            
            for item in items:
                wrapped_lines = textwrap.wrap(item, width=98)
                for line in wrapped_lines:
                    is_bullet = line.startswith("•") or line.startswith("  -") or line.startswith("Q") or line.startswith("Ans")
                    color = '#1C1917' if is_bullet else '#4A4238'
                    fontweight = 'semibold' if line.startswith("Q") else ('normal' if not is_bullet else 'medium')
                    fontsize = 8.0 if is_bullet else 7.8
                    ax.text(0.07, y_cursor, line, color=color, fontsize=fontsize, fontweight=fontweight, fontfamily='sans-serif', va='top', transform=ax.transAxes)
                    y_cursor -= 0.016
            y_cursor -= 0.012
            
        # Footer
        footer_text = f"Debris Careers • Academic College Project & Viva Guide • Page {page_idx + 1} of {len(PAGES_DATA)}"
        ax.text(0.50, 0.045, footer_text, color='#8C8074', fontsize=7.5, ha='center', va='center', transform=ax.transAxes)
        
        pdf.savefig(fig, dpi=300)
        plt.close(fig)
        
    pdf.close()
    print("PDF successfully generated at:", PDF_PATH)

if __name__ == "__main__":
    generate_pdf()
