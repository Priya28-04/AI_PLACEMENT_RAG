# 🎯 AI Placement Preparation Assistant (RAG)

An AI-powered Placement Preparation Assistant built using **Streamlit**, **LangChain**, **Groq LLM**, **FAISS**, and **HuggingFace Embeddings**. The application helps students prepare for technical interviews through Retrieval-Augmented Generation (RAG), AI-generated quizzes, mock interviews, resume analysis, and personalized study roadmaps.

---

## 🚀 Features

### 💬 AI Placement Chat (RAG)
- Ask technical interview questions.
- Retrieves relevant information from your placement PDFs.
- Generates accurate responses using Groq LLM.
- Displays the source PDF and page number for transparency.

### 📝 AI Quiz Generator
- Generate quizzes based on selected topics.
- Interactive multiple-choice questions.
- Automatic scoring.
- Displays explanations for correct answers.

### 🎤 AI Mock Interview
- Generates 5 interview questions based on the selected role.
- User types answers for each question.
- AI evaluates every answer.
- Provides:
  - Score
  - Strengths
  - Weaknesses
  - Missing Concepts
  - Ideal Answer
  - Suggestions for Improvement
- Final interview performance report.

### 📄 Resume Analyzer
- Upload your resume in PDF format.
- AI analyzes your resume.
- Provides:
  - ATS Suggestions
  - Strengths
  - Weaknesses
  - Missing Skills
  - Improvement Recommendations

### 📅 Study Roadmap
- Generates a personalized preparation roadmap.
- Covers:
  - Data Structures & Algorithms
  - DBMS
  - Operating Systems
  - Computer Networks
  - OOP
  - SQL
  - Aptitude
  - HR Interview Preparation

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | User Interface |
| LangChain | LLM Framework |
| Groq | Large Language Model |
| HuggingFace | Embeddings |
| FAISS | Vector Database |
| PyPDF | PDF Text Extraction |
| Python Dotenv | Environment Variables |

---

# 📂 Project Structure

```
AI_PLACEMENT_RAG/
│
├── app.py
├── create_vectorstore.py
├── requirements.txt
├── .env
│
├── data/
│   └── pdfs/
│       ├── ALGORITHMS.pdf
│       ├── ARRAYS.pdf
│       ├── BACKTRACKING.pdf
│       ├── BINARY SEARCH TREE.pdf
│       ├── BINARY TREE.pdf
│       ├── DIVIDE & CONQUER.pdf
│       ├── DYNAMIC PROGRAMMING.pdf
│       ├── GRAPHS.pdf
│       ├── GREEDY.pdf
│       ├── HEAP.pdf
│       ├── LINKED LIST.pdf
│       ├── MATRIX.pdf
│       ├── PUZZLES.pdf
│       ├── QUEUE.pdf
│       ├── SORTING.pdf
│       ├── STACK.pdf
│       ├── STRING.pdf
│       ├── TIME COMPLEXITIES.pdf
│       └── TRIE.pdf
│
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
│
└── utils/
    ├── rag.py
    ├── quiz.py
    ├── interview.py
    ├── roadmap.py
    └── resume.py
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/AI_PLACEMENT_RAG.git
cd AI_PLACEMENT_RAG
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

Using pip

```bash
pip install -r requirements.txt
```

Using uv

```bash
uv pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

# 📚 Prepare the Knowledge Base

Place all PDF notes inside:

```
data/pdfs/
```

---

# 🧠 Build the Vector Database

```bash
python create_vectorstore.py
```

This creates:

```
faiss_index/
```

which stores the embeddings and vector index used by the chatbot.

---

# ▶️ Run the Application

Using Streamlit:

```bash
streamlit run app1.py
```

Using uv:

```bash
uv run streamlit run app1.py
```

---

# 📖 Topics Covered

The knowledge base includes interview preparation material for:

- Algorithms
- Arrays
- Backtracking
- Binary Search
- Binary Search Tree
- Binary Tree
- Divide & Conquer
- Dynamic Programming
- Graphs
- Greedy Algorithms
- Heap
- Linked List
- Matrix
- Queue
- Sorting
- Stack
- String
- Time Complexity
- Trie

---

# 🔄 Application Workflow

```
             User
               │
               ▼
      Streamlit Interface
               │
               ▼
         FAISS Retriever
               │
               ▼
 Relevant PDF Chunks Retrieved
               │
               ▼
          Groq LLM
               │
               ▼
      AI Generated Response
```

---

# 💡 Sample Questions

### AI Chat

- Explain Merge Sort.
- What is Dynamic Programming?
- Explain Graph Traversal.
- Difference between Stack and Queue.
- Explain Trie.

### Quiz

- Generate a quiz on Graphs.
- Generate 10 questions on Arrays.

### Mock Interview

- Conduct a Software Engineer interview.
- Conduct an AI Engineer interview.

### Resume Analyzer

- Analyze my resume.
- Suggest ATS improvements.

### Roadmap

- Generate a 30-day placement roadmap.
- Create a roadmap for AI Engineer preparation.

---

# 📈 Future Enhancements

- User Authentication
- Performance Dashboard
- Adaptive Quiz Difficulty
- Company-wise Interview Questions
- Voice-based Mock Interviews
- Progress Tracking
- Chat History Export
- Gamification & Leaderboard
- Online PDF Upload
- Multi-language Support

---

# 📷 Screenshots

Add screenshots of:

- Home Page
- AI Chat
- Quiz Generator
- Mock Interview
- Resume Analyzer
- Study Roadmap

---

# 👨‍💻 Author

Priyanka L Hittalamani

Computer Science Engineering Student

AI • Machine Learning • Generative AI Enthusiast

---

# 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
