import os
import re
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from utils.rag import ask_question
from utils.quiz import generate_quiz
from utils.interview import (
    generate_questions,
    evaluate_answer,
)
from utils.roadmap import generate_roadmap
from utils.resume import analyze_resume

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

# ----------------------------------------------------
# Streamlit Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Placement HQ | AI Prep Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------
# Design System — "Mission Control for Placements"
# ----------------------------------------------------
# Palette: cool paper background, electric-indigo primary,
# coral for urgency/incorrect, mint for correct/success,
# gold for streaks & achievement.
# Type: Space Grotesk (display) + Inter (body) + JetBrains Mono (stats/scores)

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

        :root{
            --bg:#F4F6FB;
            --panel:#FFFFFF;
            --ink:#131B2E;
            --ink-soft:#5B6478;
            --primary:#3654FF;
            --primary-dark:#1F35B0;
            --coral:#FF5D73;
            --mint:#12B76A;
            --gold:#FFB020;
            --border:#E3E7F1;
        }

        html, body, [class*="css"] { font-family:'Inter', sans-serif; color:var(--ink); }
        .stApp { background:var(--bg); }

        /* ---- Typography helpers ---- */
        .display-font { font-family:'Space Grotesk', sans-serif; }
        .mono-font { font-family:'JetBrains Mono', monospace; }

        /* ---- Hide default Streamlit chrome ---- */
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header[data-testid="stHeader"] { background:transparent; }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background:linear-gradient(180deg, #131B2E 0%, #1B2540 100%);
            border-right:1px solid #0B1120;
        }
        section[data-testid="stSidebar"] * { color:#E7EAF5 !important; }
        section[data-testid="stSidebar"] .sidebar-brand {
            padding:6px 4px 18px 4px;
            border-bottom:1px solid rgba(255,255,255,0.08);
            margin-bottom:14px;
        }
        section[data-testid="stSidebar"] .sidebar-brand-title {
            font-family:'Space Grotesk', sans-serif;
            font-weight:700;
            font-size:22px;
            letter-spacing:0.2px;
        }
        section[data-testid="stSidebar"] .sidebar-brand-sub {
            font-size:12.5px;
            color:#9AA4C4 !important;
            margin-top:2px;
        }
        section[data-testid="stSidebar"] .stRadio > label { font-weight:600 !important; }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            padding:9px 10px;
            border-radius:10px;
            margin-bottom:2px;
            transition:background .15s ease;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background:rgba(255,255,255,0.06);
        }
        section[data-testid="stSidebar"] input[type="radio"] { accent-color:var(--gold); }

        .chip-row { display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }
        .chip {
            font-family:'JetBrains Mono', monospace;
            font-size:11px;
            font-weight:700;
            padding:5px 9px;
            border-radius:999px;
            background:rgba(54,84,255,0.18);
            color:#B9C4FF !important;
            border:1px solid rgba(54,84,255,0.35);
        }

        /* ---- Buttons ---- */
        .stButton>button {
            background:linear-gradient(90deg, var(--primary), var(--primary-dark));
            color:#fff;
            border:none;
            border-radius:12px;
            padding:0.55em 1.4em;
            font-weight:700;
            font-family:'Space Grotesk', sans-serif;
            letter-spacing:0.2px;
            box-shadow:0 6px 16px rgba(54,84,255,0.25);
            transition:transform .12s ease, box-shadow .12s ease;
        }
        .stButton>button:hover {
            transform:translateY(-2px);
            box-shadow:0 10px 22px rgba(54,84,255,0.32);
            color:#fff;
        }
        .stButton>button:active { transform:translateY(0px); }

        /* ---- Section banner ---- */
        .section-banner {
            display:flex; align-items:center; gap:16px;
            background:var(--panel);
            border:1px solid var(--border);
            border-left:6px solid var(--accent, var(--primary));
            border-radius:16px;
            padding:18px 22px;
            margin-bottom:22px;
            box-shadow:0 2px 12px rgba(19,27,46,0.05);
        }
        .section-icon { font-size:32px; line-height:1; }
        .section-title {
            font-family:'Space Grotesk', sans-serif;
            font-size:22px; font-weight:700; color:var(--ink);
        }
        .section-subtitle { color:var(--ink-soft); font-size:14px; margin-top:2px; }

        /* ---- Cards ---- */
        .feature-card {
            background:var(--panel);
            border:1px solid var(--border);
            border-radius:16px;
            padding:20px;
            height:100%;
            transition:transform .15s ease, box-shadow .15s ease;
            box-shadow:0 2px 10px rgba(19,27,46,0.04);
        }
        .feature-card:hover {
            transform:translateY(-4px);
            box-shadow:0 12px 24px rgba(19,27,46,0.10);
        }
        .feature-icon {
            font-size:28px;
            width:48px; height:48px;
            display:flex; align-items:center; justify-content:center;
            border-radius:12px;
            background:var(--tint, rgba(54,84,255,0.10));
            margin-bottom:12px;
        }
        .feature-title { font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:17px; margin-bottom:4px; }
        .feature-desc { color:var(--ink-soft); font-size:13.5px; line-height:1.5; }

        /* ---- Badges (score tiers) ---- */
        .badge-pill {
            display:inline-block;
            padding:6px 16px;
            border-radius:999px;
            font-family:'JetBrains Mono', monospace;
            font-weight:700;
            font-size:13px;
            background:rgba(0,0,0,0.03);
            border:1.5px solid var(--b, var(--primary));
            color:var(--b, var(--primary));
        }

        /* ---- Hero ---- */
        .hero-wrap {
            background:linear-gradient(135deg, #131B2E 0%, #21306B 55%, #3654FF 100%);
            border-radius:24px;
            padding:42px 40px;
            margin-bottom:28px;
            position:relative;
            overflow:hidden;
        }
        .hero-eyebrow {
            font-family:'JetBrains Mono', monospace;
            color:#B9C4FF;
            font-size:13px;
            font-weight:700;
            letter-spacing:1.5px;
            text-transform:uppercase;
        }
        .hero-title {
            font-family:'Space Grotesk', sans-serif;
            font-weight:700;
            font-size:44px;
            line-height:1.08;
            color:#FFFFFF;
            margin:10px 0 12px 0;
        }
        .hero-sub { color:#C7CEEA; font-size:15.5px; max-width:560px; line-height:1.55; }

        /* ---- Gauge ---- */
        .gauge {
            width:168px; height:168px; border-radius:50%;
            display:flex; align-items:center; justify-content:center;
            margin:0 auto;
        }
        .gauge-inner {
            width:132px; height:132px; border-radius:50%;
            background:#131B2E;
            display:flex; flex-direction:column; align-items:center; justify-content:center;
        }
        .gauge-pct { font-family:'Space Grotesk', sans-serif; font-size:30px; font-weight:700; color:#fff; }
        .gauge-label { font-family:'JetBrains Mono', monospace; font-size:11px; color:#B9C4FF; letter-spacing:1px; }

        /* ---- Metric-style stat card ---- */
        .stat-card {
            background:rgba(255,255,255,0.07);
            border:1px solid rgba(255,255,255,0.14);
            border-radius:14px;
            padding:14px 16px;
            text-align:center;
        }
        .stat-num { font-family:'JetBrains Mono', monospace; font-size:22px; font-weight:700; color:#fff; }
        .stat-lbl { font-size:11.5px; color:#B9C4FF; letter-spacing:0.4px; margin-top:2px; }

        hr { border-color:var(--border) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_banner(icon, title, subtitle, color="#3654FF"):
    st.markdown(
        f"""
        <div class="section-banner" style="--accent:{color}">
            <div class="section-icon">{icon}</div>
            <div>
                <div class="section-title">{title}</div>
                <div class="section-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text, color):
    st.markdown(
        f'<span class="badge-pill" style="--b:{color}">{text}</span>',
        unsafe_allow_html=True,
    )


def tier_color(pct, high=90, mid=70, low=50):
    if pct >= high:
        return "#12B75E", "🌟 Excellent Performance!"
    elif pct >= mid:
        return "#3654FF", "👍 Good Job!"
    elif pct >= low:
        return "#FFB020", "📚 Keep Practicing!"
    else:
        return "#FF5D73", "💡 You need more practice."


inject_css()

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

defaults = {
    "chat_history": [],
    "quiz": None,
    "quiz_submitted": False,
    "questions": [],
    "current_question": 0,
    "interview_answers": [],
    "interview_feedback": [],
    "scores": [],
    "feedbacks": [],
    "interview_started": False,
    "answer_submitted": False,
    "current_feedback": "",
    "interview_completed": False,
    "roadmap_generated": False,
    "resume_analyzed": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🚀 Placement HQ</div>
            <div class="sidebar-brand-sub">Your AI-powered prep command center</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    menu = st.radio(
        "Choose Feature",
        [
            "🏠 Home",
            "💬 AI Chat",
            "📝 Quiz Generator",
            "🎤 Mock Interview",
            "📅 Study Roadmap",
            "📄 Resume Analyzer",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:12px; color:#9AA4C4; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:2px;">Powered by</div>
        <div class="chip-row">
            <span class="chip">LangChain</span>
            <span class="chip">FAISS</span>
            <span class="chip">HuggingFace</span>
            <span class="chip">Groq</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:12px; color:#9AA4C4;">
            🚀 Placement HQ · v1.0<br>
            Built with Streamlit · LangChain · HuggingFace · FAISS · Groq
        </div>
        """,
        unsafe_allow_html=True,
    )

# ====================================================
# HOME / DASHBOARD
# ====================================================

if menu == "🏠 Home":

    quiz_pct = None
    if st.session_state.quiz_submitted and st.session_state.quiz:
        # best-effort recompute isn't stored, so just mark completion
        quiz_pct = 100

    features_done = sum(
        [
            bool(st.session_state.quiz_submitted),
            bool(st.session_state.interview_completed),
            bool(st.session_state.roadmap_generated),
            bool(st.session_state.resume_analyzed),
        ]
    )
    readiness_pct = int(round((features_done / 4) * 100))

    col_hero, col_gauge = st.columns([2.1, 1])

    with col_hero:
        st.markdown(
            f"""
            <div class="hero-wrap">
                <div class="hero-eyebrow">AI PLACEMENT PREPARATION ASSISTANT</div>
                <div class="hero-title">Train like it's<br>interview day.</div>
                <div class="hero-sub">
                    Ask DSA doubts, grind topic-wise quizzes, run mock interviews with instant
                    feedback, generate a day-by-day roadmap, and get your resume reviewed —
                    all powered by your own placement material.
                </div>
                <div style="display:flex; gap:12px; margin-top:22px; flex-wrap:wrap;">
                    <div class="stat-card" style="flex:1; min-width:120px;">
                        <div class="stat-num">{len(st.session_state.get('quiz') or [])}</div>
                        <div class="stat-lbl">QUIZ QUESTIONS</div>
                    </div>
                    <div class="stat-card" style="flex:1; min-width:120px;">
                        <div class="stat-num">{len(st.session_state.scores)}</div>
                        <div class="stat-lbl">INTERVIEW ANSWERS</div>
                    </div>
                    <div class="stat-card" style="flex:1; min-width:120px;">
                        <div class="stat-num">{features_done}/4</div>
                        <div class="stat-lbl">TOOLS EXPLORED</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_gauge:
        st.markdown(
            f"""
            <div class="hero-wrap" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:30px 20px;">
                <div class="gauge" style="background:conic-gradient(var(--gold) {readiness_pct}%, rgba(255,255,255,0.15) 0);">
                    <div class="gauge-inner">
                        <div class="gauge-pct">{readiness_pct}%</div>
                        <div class="gauge-label">READINESS</div>
                    </div>
                </div>
                <div style="color:#C7CEEA; font-size:12.5px; margin-top:14px; text-align:center;">
                    Based on tools used this session
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🧭 Explore the toolkit")

    cards = [
        ("💬", "AI Chat", "Ask topic-wise DSA & placement questions, answered straight from your own knowledge base.", "#3654FF", "rgba(54,84,255,0.10)"),
        ("📝", "Quiz Generator", "Timed, topic-specific MCQs with instant scoring and explanations.", "#12B75E", "rgba(18,183,94,0.10)"),
        ("🎤", "Mock Interview", "Role-based interview questions with AI feedback and a 10-point score.", "#FF5D73", "rgba(255,93,115,0.10)"),
        ("📅", "Study Roadmap", "A personalized day-by-day plan built around your prep timeline.", "#FFB020", "rgba(255,176,32,0.12)"),
        ("📄", "Resume Analyzer", "Upload your resume and get structured, actionable feedback.", "#7C5CFF", "rgba(124,92,255,0.10)"),
        ("🏆", "Track Progress", "Your readiness score above updates as you use each tool.", "#0EA5E9", "rgba(14,165,233,0.10)"),
    ]

    for row_start in range(0, len(cards), 3):
        row = cards[row_start:row_start + 3]
        cols = st.columns(3)
        for c, (icon, title, desc, color, tint) in zip(cols, row):
            with c:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-icon" style="--tint:{tint}; color:{color};">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='margin-top:10px; color:#5B6478; font-size:13px;'>👈 Pick a tool from the sidebar to get started.</div>", unsafe_allow_html=True)

# ====================================================
# AI CHAT (RAG)
# ====================================================

elif menu == "💬 AI Chat":

    section_banner("💬", "Placement Assistant", "Ask anything from your placement knowledge base, filtered by topic.", "#3654FF")

    topic = st.selectbox(
        "Choose Topic",
        [
            "All",
            "ALGORITHMS",
            "ARRAYS",
            "BACKTRACKING",
            "BINARY",
            "BINARY SEARCH TREE",
            "BINARY TREE",
            "DIVIDE & CONQUER",
            "DYNAMIC PROGRAMMING",
            "GRAPHS",
            "GREEDY",
            "HEAP",
            "LINKED LIST",
            "MATRIX",
            "PUZZLES",
            "QUEUE",
            "SORTING",
            "STACK",
            "STRING",
            "TIME COMPLEXITIES",
            "TRIE",
        ],
    )

    question = st.text_input(
        "Ask your placement question..."
    )

    if st.button("🚀 Get Answer"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching Knowledge Base..."):

                answer, docs = ask_question(
                    question,
                    topic,
                )

            st.session_state.chat_history.append(
                ("You", question)
            )

            st.session_state.chat_history.append(
                ("Assistant", answer)
            )

            st.success(answer)

            st.divider()

            st.subheader("📚 Reference Sources")

            shown = set()

            for doc in docs:

                source = os.path.basename(
                    doc.metadata["source"]
                )

                page = doc.metadata["page"] + 1

                key = (source, page)

                if key not in shown:

                    shown.add(key)

                    st.write(
                        f"📄 **{source}** (Page {page})"
                    )

    st.divider()

    st.subheader("💬 Conversation")

    if len(st.session_state.chat_history) == 0:

        st.info("No conversation yet.")

    else:

        for role, message in st.session_state.chat_history:

            if role == "You":

                with st.chat_message("user"):

                    st.write(message)

            else:

                with st.chat_message("assistant"):

                    st.write(message)

# ====================================================
# QUIZ GENERATOR
# ====================================================

elif menu == "📝 Quiz Generator":

    section_banner("📝", "AI Placement Quiz", "Topic-wise MCQs with instant scoring and explanations.", "#12B75E")

    topic = st.selectbox(
        "Choose Topic",
        [
            "Arrays",
            "Stack",
            "Queue",
            "Linked List",
            "Tree",
            "Graph",
            "Greedy",
            "Dynamic Programming",
            "Trie",
            "Heap",
            "Sorting",
            "Matrix"
        ]
    )

    num_questions = st.selectbox(
        "Number of Questions",
        [5, 10, 15]
    )

    # -----------------------------
    # Generate Quiz
    # -----------------------------

    if st.button("🎯 Generate Quiz"):

        with st.spinner("Generating Quiz..."):

            st.session_state.quiz = generate_quiz(
                topic,
                num_questions
            )

            st.session_state.quiz_submitted = False

    # -----------------------------
    # Display Quiz
    # -----------------------------

    if st.session_state.quiz:

        user_answers = {}

        st.divider()

        for i, q in enumerate(st.session_state.quiz):

            st.subheader(f"Question {i+1}")

            st.write(q["question"])

            user_answers[i] = st.radio(

                "Choose Answer",

                options=["A", "B", "C", "D"],

                format_func=lambda x: f"{x}. {q['options'][x]}",

                key=f"quiz_{i}"

            )

        # -----------------------------
        # Submit Quiz
        # -----------------------------

        if st.button("✅ Submit Quiz"):

            st.session_state.quiz_submitted = True

            score = 0

            st.divider()

            st.header("📊 Quiz Result")

            for i, q in enumerate(st.session_state.quiz):

                st.subheader(f"Question {i+1}")

                st.write(q["question"])

                if user_answers[i] == q["answer"]:

                    score += 1

                    st.success("✅ Correct")

                else:

                    st.error("❌ Incorrect")

                    st.write(
                        f"**Correct Answer:** "
                        f"{q['answer']} - "
                        f"{q['options'][q['answer']]}"
                    )

                st.info(q["explanation"])

            percentage = round(
                (score / len(st.session_state.quiz)) * 100,
                2
            )

            st.divider()

            m1, m2 = st.columns(2)
            with m1:
                st.metric("Final Score", f"{score}/{len(st.session_state.quiz)}")
            with m2:
                st.metric("Percentage", f"{percentage}%")

            color, message = tier_color(percentage)
            badge(message, color)

        # -----------------------------
        # Restart Quiz
        # -----------------------------

        if st.session_state.quiz_submitted:

            if st.button("🔄 Restart Quiz"):

                st.session_state.quiz = None
                st.session_state.quiz_submitted = False

                st.rerun()

# ====================================================
# MOCK INTERVIEW
# ====================================================

elif menu == "🎤 Mock Interview":

    section_banner("🎤", "AI Mock Interview", "Role-based questions with AI feedback and scoring.", "#FF5D73")

    role = st.selectbox(
        "Select Role",
        [
            "Python Developer",
            "AI Engineer",
            "Software Engineer",
            "Data Scientist"
        ]
    )

    # ----------------------------
    # Start Interview
    # ----------------------------

    if not st.session_state.interview_started:

        if st.button("🚀 Start Interview"):

            with st.spinner("Generating Interview Questions..."):

                st.session_state.questions = generate_questions(role)

            st.session_state.current_question = 0
            st.session_state.feedbacks = []
            st.session_state.scores = []
            st.session_state.answer_submitted = False
            st.session_state.current_feedback = ""
            st.session_state.interview_started = True
            st.session_state.interview_completed = False

            st.rerun()

    # ----------------------------
    # Interview Running
    # ----------------------------

    if st.session_state.interview_started:

        q_no = st.session_state.current_question
        total = len(st.session_state.questions)

        if q_no < total:

            question = st.session_state.questions[q_no]

            st.progress((q_no + 1) / total)

            st.subheader(f"Question {q_no + 1} of {total}")

            st.info(question)

            answer = st.text_area(
                "Write your answer",
                height=220,
                key=f"answer_{q_no}"
            )

            # ------------------------
            # Submit Answer
            # ------------------------

            if not st.session_state.answer_submitted:

                if st.button("✅ Submit Answer"):

                    if answer.strip() == "":

                        st.warning("Please write your answer.")

                    else:

                        with st.spinner("Evaluating..."):

                            feedback = evaluate_answer(
                                question,
                                answer
                            )

                        st.session_state.current_feedback = feedback
                        st.session_state.feedbacks.append(feedback)

                        score = 0

                        match = re.search(r"(\d+)/10", feedback)

                        if match:
                            score = int(match.group(1))

                        st.session_state.scores.append(score)

                        st.session_state.answer_submitted = True

                        st.rerun()

            # ------------------------
            # Feedback
            # ------------------------

            if st.session_state.answer_submitted:

                st.success("Answer Evaluated Successfully")

                st.write(st.session_state.current_feedback)

                # ------------------------
                # Next Question
                # ------------------------

                if q_no < total - 1:

                    if st.button("➡ Next Question"):

                        st.session_state.current_question += 1
                        st.session_state.answer_submitted = False
                        st.session_state.current_feedback = ""

                        st.rerun()

                else:

                    if st.button("🏁 Finish Interview"):

                        st.session_state.current_question += 1
                        st.session_state.answer_submitted = False
                        st.session_state.interview_completed = True

                        st.rerun()

        # ----------------------------
        # Final Report
        # ----------------------------

        else:

            st.balloons()

            st.header("🎉 Interview Completed")

            avg = round(
                sum(st.session_state.scores) /
                len(st.session_state.scores),
                2
            )

            st.metric(
                "Overall Score",
                f"{avg}/10"
            )

            color, message = tier_color(avg, high=9, mid=8, low=6)
            badge(message, color)

            st.divider()

            st.subheader("Detailed Feedback")

            for i, feedback in enumerate(st.session_state.feedbacks):

                with st.expander(f"Question {i+1}"):

                    st.write(feedback)

            if st.button("🔄 Restart Interview"):

                st.session_state.questions = []
                st.session_state.current_question = 0
                st.session_state.feedbacks = []
                st.session_state.scores = []
                st.session_state.current_feedback = ""
                st.session_state.answer_submitted = False
                st.session_state.interview_started = False
                st.session_state.interview_completed = False

                st.rerun()

# ====================================================
# STUDY ROADMAP
# ====================================================

elif menu == "📅 Study Roadmap":

    section_banner("📅", "AI Placement Study Roadmap", "A personalized day-by-day plan tuned to your timeline.", "#FFB020")

    col1, col2 = st.columns(2)

    with col1:

        days = st.slider(
            "Preparation Duration (Days)",
            7,
            180,
            30
        )

    with col2:

        role = st.selectbox(
            "Target Role",
            [
                "Software Engineer",
                "Python Developer",
                "AI Engineer",
                "Data Scientist",
                "Full Stack Developer"
            ]
        )

    if st.button("Generate Roadmap"):

        with st.spinner("Generating Personalized Roadmap..."):

            roadmap = generate_roadmap(days)

        st.session_state.roadmap_generated = True

        st.success("Roadmap Generated Successfully!")

        st.write(roadmap)

# ====================================================
# RESUME ANALYZER
# ====================================================

elif menu == "📄 Resume Analyzer":

    section_banner("📄", "AI Resume Analyzer", "Upload your resume for structured, actionable feedback.", "#7C5CFF")

    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["pdf"]
    )

    if uploaded_file:

        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:

                resume_text += text

        st.success("Resume Uploaded Successfully")

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing Resume..."):

                result = analyze_resume(
                    resume_text
                )

            st.session_state.resume_analyzed = True

            st.subheader("Resume Analysis")

            st.write(result)