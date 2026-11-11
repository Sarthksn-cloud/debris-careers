"""
Generate Microsoft Innovate 2026 Hackathon Presentation PDF for DEBRIS CAREERS
Matches the Bennett University / Microsoft template format, layout, cards, and typography.
Exports both the complete 6-slide PDF and high-resolution 16:9 PNG slide images.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

# Configure clean font rendering
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'

BASE_DIR = "/Users/sarthksn/.gemini/antigravity/scratch/debris-careers"
PDF_OUTPUT = os.path.join(BASE_DIR, "Debris_Careers_Microsoft_Innovate_2026_Presentation.pdf")
SLIDES_DIR = os.path.join(BASE_DIR, "presentation_slides")

# 16:9 Widescreen aspect ratio
FIG_WIDTH = 16
FIG_HEIGHT = 9

def draw_vector_rocket(ax, cx, cy):
    """Draws a clean vector rocket icon centered at (cx, cy)"""
    # Main rocket body (white)
    ax.add_patch(patches.Polygon([[cx, cy + 2.8], [cx - 1.2, cy - 0.2], [cx + 1.2, cy - 0.2]], facecolor='#ffffff', edgecolor='none'))
    ax.add_patch(patches.Rectangle((cx - 1.2, cy - 2.0), 2.4, 1.8, facecolor='#ffffff', edgecolor='none'))
    # Left fin
    ax.add_patch(patches.Polygon([[cx - 1.2, cy - 0.5], [cx - 2.5, cy - 2.2], [cx - 1.2, cy - 2.2]], facecolor='#38bdf8', edgecolor='none'))
    # Right fin
    ax.add_patch(patches.Polygon([[cx + 1.2, cy - 0.5], [cx + 2.5, cy - 2.2], [cx + 1.2, cy - 2.2]], facecolor='#38bdf8', edgecolor='none'))
    # Cabin porthole
    ax.add_patch(patches.Circle((cx, cy + 0.6), radius=0.65, facecolor='#0284c7', edgecolor='none'))
    # Engine exhaust flame
    ax.add_patch(patches.Polygon([[cx - 0.7, cy - 2.0], [cx, cy - 3.2], [cx + 0.7, cy - 2.0]], facecolor='#f59e0b', edgecolor='none'))


def create_slide_1(fig):
    """Slide 1: Title & Hackathon Metadata (Dark Navy Theme)"""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#0f1b2d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top White Banner
    top_bar = patches.Rectangle((0, 87), 100, 13, facecolor='#ffffff', edgecolor='none')
    ax.add_patch(top_bar)

    # University & Microsoft Text on Top Banner
    ax.text(3, 94.5, "BENNETT", fontsize=16, fontweight='bold', color='#c21c24')
    ax.text(3, 91.5, "UNIVERSITY", fontsize=11, fontweight='bold', color='#1e293b')
    ax.text(3, 88.5, "THE TIMES GROUP", fontsize=8, color='#475569')

    # NAAC Grade Badge
    naac_box = patches.FancyBboxPatch((13, 89), 7.5, 8.5, boxstyle="round,pad=0.2", facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=1)
    ax.add_patch(naac_box)
    ax.text(13.5, 94, "NAAC", fontsize=7.5, fontweight='bold', color='#0284c7')
    ax.text(13.5, 91.5, "GRADE", fontsize=6.5, color='#0284c7')
    ax.text(18, 91.5, "A+", fontsize=16, fontweight='bold', color='#dc2626')

    # Microsoft 4-square logo
    ms_x = 22.5
    ax.add_patch(patches.Rectangle((ms_x, 93.8), 1.5, 1.5, facecolor='#f25022', edgecolor='none'))
    ax.add_patch(patches.Rectangle((ms_x + 1.8, 93.8), 1.5, 1.5, facecolor='#7fba00', edgecolor='none'))
    ax.add_patch(patches.Rectangle((ms_x, 91.8), 1.5, 1.5, facecolor='#00a4ef', edgecolor='none'))
    ax.add_patch(patches.Rectangle((ms_x + 1.8, 91.8), 1.5, 1.5, facecolor='#ffb900', edgecolor='none'))
    ax.text(ms_x + 4, 92.5, "Microsoft", fontsize=18, fontweight='semibold', color='#505050')

    # School Name on Top Right
    ax.text(97, 93, "School of Computer Science Engineering & Technology", fontsize=12, fontweight='bold', color='#c21c24', ha='right')

    # Main Hackathon Header
    ax.text(4, 79, "M I C R O S O F T   P O W E R E D   H A C K A T H O N", fontsize=11, fontweight='bold', color='#38bdf8')
    ax.text(4, 71, "Microsoft Innovate 2026", fontsize=34, fontweight='bold', color='#ffffff')
    ax.text(4, 65.5, "Innovate  ·  Build  ·  Empower", fontsize=15, fontstyle='italic', color='#94a3b8')

    # Metadata Form Fields (Dark Blue Cards)
    fields = [
        ("Team Name", "Debris"),
        ("Team ID", "506"),
        ("Problem Statement Title", "Debris Careers — Intelligent Career Guidance & Stream Navigation Assistant"),
        ("Theme / Bucket", "Smart Assistants & Chatbots"),
        ("Team Leader", "Sarthak Soni, A26BSCAIU0010, A26BSCAIU0010@bennett.edu.in")
    ]

    y_pos = 53
    for label, val in fields:
        ax.text(4, y_pos + 1.8, label, fontsize=12.5, fontweight='bold', color='#cbd5e1')
        field_box = patches.FancyBboxPatch((28, y_pos - 0.5), 40, 5.5, boxstyle="round,pad=0.3", facecolor='#162842', edgecolor='#1e3a5f', lw=1.2)
        ax.add_patch(field_box)
        # Handle long text
        display_val = val if len(val) < 55 else val[:52] + "..."
        ax.text(29.5, y_pos + 1.8, display_val, fontsize=11.5, fontweight='bold', color='#f8fafc')
        y_pos -= 9.5

    # Right Rocket Badge
    circle_badge = patches.Circle((85, 60), radius=5.8, facecolor='#0284c7', edgecolor='#38bdf8', lw=1.5)
    ax.add_patch(circle_badge)
    draw_vector_rocket(ax, 85, 60)

    ax.text(85, 48, "ROUND 1", fontsize=22, fontweight='bold', color='#ffffff', ha='center')
    ax.text(85, 43, "Idea Submission", fontsize=13, color='#94a3b8', ha='center')


def draw_slide_header_and_footer(ax, title, slide_num):
    """Standard header and footer for slides 2-6"""
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Slide Title
    ax.text(4, 91, title, fontsize=28, fontweight='bold', color='#0f172a')
    # Round subtitle on top right
    ax.text(96, 91, "Round 1 – Idea Submission", fontsize=12, color='#64748b', ha='right')

    # Footer
    footer_text = f"Debris | Microsoft Innovate 2026 · Bennett University | Slide {slide_num} of 6"
    ax.text(4, 3, footer_text, fontsize=9.5, color='#94a3b8')


def create_slide_2(fig):
    """Slide 2: Team Details"""
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide_header_and_footer(ax, "Team Details", 2)

    # Table coordinates
    x_start = 4
    x_end = 96
    y_top = 80
    row_height = 9.5

    cols = [
        ("S. No.", 8),
        ("Full Name", 18),
        ("Enrollment No.", 18),
        ("Programme & Year", 18),
        ("Email", 22),
        ("Role in Team", 16)
    ]

    # Draw Header Row (Dark Blue)
    header_box = patches.FancyBboxPatch((x_start, y_top - row_height), x_end - x_start, row_height, boxstyle="round,pad=0.1", facecolor='#0a192f', edgecolor='#0a192f')
    ax.add_patch(header_box)

    cur_x = x_start
    for name, width in cols:
        ax.text(cur_x + width/2, y_top - row_height/2 - 0.5, name, fontsize=11.5, fontweight='bold', color='#ffffff', ha='center', va='center')
        cur_x += width

    # Data Rows
    team_data = [
        ("1", "Sarthak Soni", "A26BSCAIU0010", "BSC AI, 1ST YEAR", "A26BSCAIU0010@bennett.edu.in", "Team Leader"),
        ("2", "Navneet Kumar", "A26BSCAIU0019", "BSC AI, 1ST YEAR", "A26BSCAIU0019@bennett.edu.in", "Designer, Research"),
        ("3", "Bhawin Sawant", "S26CSEU1816", "B.TECH CSE, 1ST YEAR", "S26CSEU1816@bennett.edu.in", "Developer, Research")
    ]

    cur_y = y_top - row_height
    for row_idx, row in enumerate(team_data):
        cur_y -= row_height
        bg_col = '#ffffff' if row_idx % 2 == 0 else '#f1f5f9'
        rbox = patches.Rectangle((x_start, cur_y), x_end - x_start, row_height, facecolor=bg_col, edgecolor='#cbd5e1', lw=0.8)
        ax.add_patch(rbox)

        cur_x = x_start
        for val_idx, val in enumerate(row):
            w = cols[val_idx][1]
            fweight = 'bold' if val_idx in [0, 1, 5] else 'normal'
            ax.text(cur_x + w/2, cur_y + row_height/2, val, fontsize=10.5, fontweight=fweight, color='#1e293b', ha='center', va='center')
            cur_x += w

    # Faculty Mentor Box at Bottom
    mentor_box = patches.FancyBboxPatch((x_start, 18), x_end - x_start, 11, boxstyle="round,pad=0.3", facecolor='#ffffff', edgecolor='#cbd5e1', lw=1.2)
    ax.add_patch(mentor_box)
    ax.text(6, 23.5, "Faculty Mentor: Deepak Dhillon, School of AI, A24SOAIP0003@bennett.edu.in", fontsize=13, fontweight='bold', color='#0f172a')


def draw_icon_circle(ax, x, y, icon_symbol, bg_color='#0284c7'):
    """Draws a clean circular icon badge with DejaVu-compatible Unicode symbol"""
    circ = patches.Circle((x, y), radius=2.3, facecolor=bg_color, edgecolor='none')
    ax.add_patch(circ)
    ax.text(x, y - 0.2, icon_symbol, fontsize=12, fontweight='bold', color='#ffffff', ha='center', va='center')


def create_slide_3(fig):
    """Slide 3: Problem Statement"""
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide_header_and_footer(ax, "Problem Statement", 3)

    # Card 1: What is the problem? (Top Left)
    card1 = patches.FancyBboxPatch((4, 48), 44, 36, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card1)
    draw_icon_circle(ax, 7.5, 79, "!")
    ax.text(11.5, 78.5, "What is the problem?", fontsize=16, fontweight='bold', color='#0f172a')

    c1_bullets = [
        "Millions face career ambiguity: Over 70% of high school\nand college students struggle with stream selection, leading to\nmisplaced degrees and high dropout rates.",
        "Static advice & information overload: Conventional guidance\nrelies on outdated articles that fail to understand a student's\nunique blend of skills, marks, and genuine passions.",
        "Scattered institutional intelligence: Cutoffs, premier colleges\n(IITs, AIIMS, NLUs, SRCC), and recruiter hiring criteria are\nfragmented across dozens of unverified portals."
    ]
    by = 72
    for b in c1_bullets:
        ax.text(7, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, by, b, fontsize=10.5, color='#334155', va='top')
        by -= 7.5

    # Card 2: Who faces it? (Top Right)
    card2 = patches.FancyBboxPatch((52, 48), 44, 36, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card2)
    draw_icon_circle(ax, 55.5, 79, "❖")
    ax.text(59.5, 78.5, "Who faces it?", fontsize=16, fontweight='bold', color='#0f172a')

    c2_bullets = [
        "High School Students (Class 10th & 12th): Confused between\nNon-Medical (STEM), Medical, Commerce, and Humanities.",
        "Undergrads & Fresh Graduates: Seeking high-growth technical\nspecializations, verified recruiter roadmaps, and salary tiers.",
        "Parents & Academic Mentors: Seeking unbiased, data-backed\ncareer guidance without predatory sales pitches from\ncommercial coaching institutes."
    ]
    by = 72
    for b in c2_bullets:
        ax.text(55, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(57, by, b, fontsize=10.5, color='#334155', va='top')
        by -= 7.5

    # Card 3: Why do current options fall short? (Bottom Wide)
    card3 = patches.FancyBboxPatch((4, 9), 92, 35, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card3)
    draw_icon_circle(ax, 7.5, 38.5, "?")
    ax.text(11.5, 38, "Why do current options fall short?", fontsize=16, fontweight='bold', color='#0f172a')

    c3_bullets = [
        "Private counsellors are costly & subjective: 1-on-1 human sessions charge ₹5,000–₹25,000 and often suffer from individual\nbias, affiliate marketing tie-ins, and lack of real-time employment data.",
        "Static tests & MCQs are rigid: Conventional aptitude questionnaires force students into artificial multiple-choice boxes\nrather than parsing free-form natural language expressions of their personal interests.",
        "Generic AI chatbots hallucinate: General-purpose LLMs frequently invent fake cutoffs, non-existent entrance requirements,\nand unverified placement statistics without strict deterministic grounding."
    ]
    by = 31
    for b in c3_bullets:
        ax.text(7, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, by, b, fontsize=10.5, color='#334155', va='top')
        by -= 7.2


def create_slide_4(fig):
    """Slide 4: Proposed Solution"""
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide_header_and_footer(ax, "Proposed Solution", 4)

    # Card 1: Our idea in one line (Top Wide)
    card1 = patches.FancyBboxPatch((4, 62), 92, 23, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card1)
    draw_icon_circle(ax, 7.5, 79.5, "★")
    ax.text(11.5, 79, "Our idea in one line", fontsize=16, fontweight='bold', color='#0f172a')

    one_liner = "• We are building Debris Careers, an intelligent NLP and Machine Learning powered Career Advisory assistant\n  that transforms free-form natural language queries into deterministic, ranked career roadmaps, college benchmarks,\n  and recruiter intelligence without forced MCQs."
    ax.text(7.5, 72.5, one_liner, fontsize=12, color='#1e293b', va='top', fontweight='medium')

    # Card 2: How it solves the problem (Bottom Left)
    card2 = patches.FancyBboxPatch((4, 9), 44, 49, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card2)
    draw_icon_circle(ax, 7.5, 52.5, "⚙")
    ax.text(11.5, 52, "How it solves the problem", fontsize=16, fontweight='bold', color='#0f172a')

    c2_bullets = [
        "Free-Form Natural Intent Understanding: Students freely\ndescribe their passions, favorite subjects, or career goals in\nnatural conversational language.",
        "Vector-Space ML Matching: TF-IDF vectorization and cosine\nsimilarity score user input against verified institutional\ncareer profiles in real-time.",
        "Complete Actionable Roadmaps: Synthesizes required academic\ndegrees, top-tier colleges, entrance exams, skills, hiring\ncompanies, and sequential next steps."
    ]
    by = 44
    for b in c2_bullets:
        ax.text(7, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, by, b, fontsize=10.5, color='#334155', va='top')
        by -= 11.5

    # Card 3: What makes it different (Bottom Right)
    card3 = patches.FancyBboxPatch((52, 9), 44, 49, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card3)
    draw_icon_circle(ax, 55.5, 52.5, "✦")
    ax.text(59.5, 52, "What makes it different", fontsize=16, fontweight='bold', color='#0f172a')

    c3_bullets = [
        "Zero Hallucination Guarantee: Combines machine learning\nranking with a deterministic knowledge base, ensuring every\nrecommended college and exam is 100% verified.",
        "Context-Aware Follow-ups: Built-in conversation memory\nremembers previously discussed careers to seamlessly answer\ntargeted follow-ups (colleges, skills, exams).",
        "Privacy-First & Fully Offline Capable: Zero reliance on paid\nexternal cloud APIs; runs locally with SQLite session\npersistence and instant chat history management."
    ]
    by = 44
    for b in c3_bullets:
        ax.text(55, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(57, by, b, fontsize=10.5, color='#334155', va='top')
        by -= 11.5


def create_slide_5(fig):
    """Slide 5: Technical Approach"""
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide_header_and_footer(ax, "Technical Approach", 5)

    # Planned Tech Stack Header
    ax.text(4, 83.5, "Planned tech stack", fontsize=16, fontweight='bold', color='#0f172a')

    # Tech stack pills
    techs = ["Python 3", "Flask Framework", "Scikit-Learn (TF-IDF)", "SQLite3 Database", "HTML5 & CSS3 Glassmorphism", "Vanilla JavaScript"]
    tx = 4
    for t in techs:
        pill_w = len(t) * 1.05 + 4
        pbox = patches.FancyBboxPatch((tx, 74.5), pill_w, 6, boxstyle="round,pad=0.3", facecolor='#ffffff', edgecolor='#0284c7', lw=1.2)
        ax.add_patch(pbox)
        ax.text(tx + pill_w/2, 77.5, t, fontsize=10.5, fontweight='bold', color='#0f172a', ha='center', va='center')
        tx += pill_w + 2.5

    # How the system will work Header
    ax.text(4, 69, "How the system will work", fontsize=16, fontweight='bold', color='#0f172a')

    # 4 Pipeline Stage Boxes
    stages = [
        ("Student asks query\nor inputs profile", "Free-form natural text\n(e.g., 'coding, AI, math,\nhigh paying jobs')", '#ffffff', '#0f172a', '#e2e8f0'),
        ("NLP preprocessor\nextracts intent", "Tokenizes input, detects\nacademic stream and\ncore interest keywords", '#ffffff', '#0f172a', '#e2e8f0'),
        ("TF-IDF Vectorizer &\nCosine Similarity", "Computes mathematical\nsimilarity against institutional\ncareer vector space", '#0284c7', '#ffffff', '#0284c7'),
        ("Advisory delivered\n& stored in SQLite", "Synthesizes ranked colleges,\nexams, and recruiters;\npersists conversation context", '#ffffff', '#0f172a', '#e2e8f0')
    ]

    bx = 4
    bw = 19.5
    bh = 17
    by = 48.5
    for i, (title_s, desc_s, bg_c, text_c, border_c) in enumerate(stages):
        box_p = patches.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.3", facecolor=bg_c, edgecolor=border_c, lw=1.5)
        ax.add_patch(box_p)
        ax.text(bx + bw/2, by + bh - 4.5, title_s, fontsize=11, fontweight='bold', color=text_c, ha='center', va='center')
        ax.text(bx + bw/2, by + 5.5, desc_s, fontsize=8.8, color=text_c if bg_c == '#0284c7' else '#475569', ha='center', va='center')

        # Arrow between boxes
        if i < 3:
            ax.annotate("", xy=(bx + bw + 4.2, by + bh/2), xytext=(bx + bw + 0.8, by + bh/2),
                        arrowprops=dict(arrowstyle="->", color='#94a3b8', lw=2))
        bx += bw + 5

    # What we have started working on (Bottom Card)
    card_work = patches.FancyBboxPatch((4, 9), 92, 34, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card_work)
    draw_icon_circle(ax, 7.5, 37.5, "⚙")
    ax.text(11.5, 37, "What we have started working on", fontsize=16, fontweight='bold', color='#0f172a')

    work_bullets = [
        "Implemented & Benchmarked Core ML Pipeline: Built the Scikit-Learn TF-IDF vectorization and cosine similarity scoring algorithm\nacross 4 primary streams (STEM, Medicine, Commerce, Humanities) with 100% deterministic ranking accuracy.",
        "Engineered Full-Stack Flask Web Application: Built secure salted SHA-256 user authentication, SQLite conversation state\npersistence, and real-time conversation deletion and history clearing endpoints.",
        "Crafted Responsive Lavender Glassmorphism UI: Implemented a minimalist, premium frontend with auto-expanding input, time-aware\ngreetings, message timestamps, thinking animation, and collapsible mobile drawer."
    ]
    wy = 30
    for b in work_bullets:
        ax.text(7, wy, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, wy, b, fontsize=10.5, color='#334155', va='top')
        wy -= 7.2


def create_slide_6(fig):
    """Slide 6: Impact and Next Steps"""
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide_header_and_footer(ax, "Impact and Next Steps", 6)

    # Card 1: Expected impact (Top Left)
    card1 = patches.FancyBboxPatch((4, 48), 44, 37, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card1)
    draw_icon_circle(ax, 7.5, 80, "▲")
    ax.text(11.5, 79.5, "Expected impact", fontsize=16, fontweight='bold', color='#0f172a')

    c1_bullets = [
        "Democratizes Career Guidance: Provides high-quality,\nunbiased career and college counselling to thousands of\nstudents completely free of charge.",
        "Reduces Course Dropouts: Accurately aligns genuine student\naptitude and interests with appropriate degrees before costly\ncollege enrollment mistakes.",
        "Saves Weeks of Manual Research: Collates entrance exams,\ncollege rankings, skills, and recruiters into structured cards."
    ]
    by = 73
    for b in c1_bullets:
        ax.text(7, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, by, b, fontsize=10.2, color='#334155', va='top')
        by -= 8

    # Card 2: Feasibility (Top Right)
    card2 = patches.FancyBboxPatch((52, 48), 44, 37, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card2)
    draw_icon_circle(ax, 55.5, 80, "✓")
    ax.text(59.5, 79.5, "Feasibility", fontsize=16, fontweight='bold', color='#0f172a')

    c2_bullets = [
        "100% Working Prototype Already Built: Backend server,\nmachine learning pipeline, database, and client interface are\nfully operational and tested today.",
        "Zero API Costs & Hardware Agnostic: Requires no paid cloud\ntokens or heavy GPUs; operates fast and efficiently on standard\nlaptop CPU hardware.",
        "Balanced 3-Member Team: Sarthak Soni (Team Lead & ML/Backend),\nNavneet Kumar (UI/UX & Research), Bhawin Sawant (Dev & Testing)."
    ]
    by = 73
    for b in c2_bullets:
        ax.text(55, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(57, by, b, fontsize=10.2, color='#334155', va='top')
        by -= 8

    # Card 3: Plan for the next round (Bottom Left)
    card3 = patches.FancyBboxPatch((4, 9), 44, 36, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card3)
    draw_icon_circle(ax, 7.5, 40, "▶")
    ax.text(11.5, 39.5, "Plan for the next round", fontsize=16, fontweight='bold', color='#0f172a')

    c3_bullets = [
        "Phase 1: Expand dataset to 100+ specialized vocational\nand emerging tech pathways (Quantum, Bio-Robotics, Fintech).",
        "Phase 2: Integrate student transcript and resume parser to\nsuggest customized career pivots based on existing coursework.",
        "Phase 3: Deploy cloud microservice with multi-region CDN\nand present live interactive demonstration to hackathon judges."
    ]
    by = 33
    for b in c3_bullets:
        ax.text(7, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(9, by, b, fontsize=10.2, color='#334155', va='top')
        by -= 8

    # Card 4: References and data sources (Bottom Right)
    card4 = patches.FancyBboxPatch((52, 9), 44, 36, boxstyle="round,pad=0.5", facecolor='#ffffff', edgecolor='#e2e8f0', lw=1.2)
    ax.add_patch(card4)
    draw_icon_circle(ax, 55.5, 40, "§")
    ax.text(59.5, 39.5, "References and data sources", fontsize=16, fontweight='bold', color='#0f172a')

    c4_bullets = [
        "Ministry of Education (NIRF India Rankings 2024–2025):\nOfficial institutional accreditation, cutoffs, and college tiers.",
        "National Career Service (NCS) & NASSCOM FutureSkills:\nSkill demand matrix and corporate compensation benchmarks.",
        "Scikit-Learn Information Retrieval Architecture:\nVector Space Models & Cosine Similarity for deterministic matching."
    ]
    by = 33
    for b in c4_bullets:
        ax.text(55, by, "•", fontsize=12, color='#0284c7', fontweight='bold')
        ax.text(57, by, b, fontsize=10.2, color='#334155', va='top')
        by -= 8


def main():
    os.makedirs(SLIDES_DIR, exist_ok=True)
    print(f"Generating Microsoft Innovate 2026 Presentation PDF at: {PDF_OUTPUT}")
    
    slide_creators = [
        (1, "Title & Metadata", create_slide_1),
        (2, "Team Details", create_slide_2),
        (3, "Problem Statement", create_slide_3),
        (4, "Proposed Solution", create_slide_4),
        (5, "Technical Approach", create_slide_5),
        (6, "Impact and Next Steps", create_slide_6)
    ]

    with PdfPages(PDF_OUTPUT) as pdf:
        for num, name, creator_fn in slide_creators:
            fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=300)
            creator_fn(fig)
            pdf.savefig(fig, facecolor=fig.get_facecolor(), edgecolor='none')
            
            # Also export high-res PNG for slide deck viewing
            png_path = os.path.join(SLIDES_DIR, f"slide_{num}.png")
            fig.savefig(png_path, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close(fig)
            print(f"✓ Slide {num} created ({name}) -> {png_path}")

    print(f"\n🎉 Presentation PDF generated successfully: {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
