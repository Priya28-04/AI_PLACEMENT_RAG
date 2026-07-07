import os
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
    page_title="AI Placement Preparation Assistant",
    page_icon="🎯",
    layout="wide"
)

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = []

if "interview_feedback" not in st.session_state:
    st.session_state.interview_feedback = []

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("🎯 AI Placement Assistant")

menu = st.sidebar.radio(
    "Choose Feature",
    [
        "💬 AI Chat",
        "📝 Quiz Generator",
        "🎤 Mock Interview",
        "📅 Study Roadmap",
        "📄 Resume Analyzer",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
Powered by

✅ LangChain

✅ FAISS

✅ HuggingFace

✅ Groq
"""
)

# ----------------------------------------------------
# Main Title
# ----------------------------------------------------

st.title("🎯 AI Placement Preparation Assistant")

st.caption(
    "Practice DSA, Prepare for Interviews, Generate Quizzes, "
    "Analyze Resume and Build a Study Roadmap."
)

# ====================================================
# AI CHAT (RAG)
# ====================================================

if menu == "💬 AI Chat":

    st.header("💬 Placement Assistant")

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

    st.header("📝 AI Placement Quiz")

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
    # Session State
    # -----------------------------

    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

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

            st.metric(
                "Final Score",
                f"{score}/{len(st.session_state.quiz)}"
            )

            st.metric(
                "Percentage",
                f"{percentage}%"
            )

            if percentage >= 90:

                st.success("🌟 Excellent Performance!")

            elif percentage >= 70:

                st.success("👍 Good Job!")

            elif percentage >= 50:

                st.warning("📚 Keep Practicing!")

            else:

                st.error("💡 You need more practice.")

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

    st.header("🎤 AI Mock Interview")

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
    # Session State
    # ----------------------------

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "scores" not in st.session_state:
        st.session_state.scores = []

    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False

    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    if "current_feedback" not in st.session_state:
        st.session_state.current_feedback = ""

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

                        import re

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

            st.divider()

            st.subheader("Detailed Feedback")

            for i, feedback in enumerate(st.session_state.feedbacks):

                with st.expander(f"Question {i+1}"):

                    st.write(feedback)

            if avg >= 9:

                st.success("🌟 Excellent Performance!")

            elif avg >= 8:

                st.success("👍 Very Good!")

            elif avg >= 6:

                st.warning("📚 Good, Keep Practicing!")

            else:

                st.error("💡 Practice More!")

            if st.button("🔄 Restart Interview"):

                st.session_state.questions = []
                st.session_state.current_question = 0
                st.session_state.feedbacks = []
                st.session_state.scores = []
                st.session_state.current_feedback = ""
                st.session_state.answer_submitted = False
                st.session_state.interview_started = False

                st.rerun() 
# ====================================================
# STUDY ROADMAP
# ====================================================

elif menu == "📅 Study Roadmap":

    st.header("📅 AI Placement Study Roadmap")

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

        st.success("Roadmap Generated Successfully!")

        st.write(roadmap)

# ====================================================
# RESUME ANALYZER
# ====================================================

elif menu == "📄 Resume Analyzer":

    st.header("📄 AI Resume Analyzer")

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

            st.subheader("Resume Analysis")

            st.write(result)

# ====================================================
# HOME PAGE
# ====================================================

if menu is None:

    st.title("AI Placement Preparation Assistant")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=150
    )

    st.markdown(
        """
## Welcome 👋

This application helps you prepare for placements.

### Features

- 💬 Placement Chatbot (RAG)

- 📝 AI Quiz Generator

- 🎤 AI Mock Interview

- 📅 Study Roadmap

- 📄 Resume Analyzer

- 📚 Uses your own placement PDFs
"""
    )

# ====================================================
# FOOTER
# ====================================================

st.sidebar.markdown("---")

st.sidebar.success("🚀 AI Placement Preparation Assistant")

st.sidebar.write("Version : 1.0")

st.sidebar.write("Built with ❤️ using")

st.sidebar.write("✅ Streamlit")

st.sidebar.write("✅ LangChain")

st.sidebar.write("✅ HuggingFace")

st.sidebar.write("✅ FAISS")

st.sidebar.write("✅ Groq")