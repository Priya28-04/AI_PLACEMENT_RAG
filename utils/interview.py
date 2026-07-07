import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0.3
)

def generate_questions(role):

    prompt = f"""
You are a senior technical interviewer.

Generate EXACTLY 5 DIFFERENT interview questions for a {role}.

Rules:
- Questions should be unique.
- Increase difficulty gradually.
- Return only the questions.
- Number them from 1 to 5.
- Do NOT provide answers.
"""

    response = llm.invoke(prompt).content

    print("\nLLM Response:\n")
    print(response)

    questions = []

    for line in response.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove numbering like:
        # 1.
        # 1)
        # - 1.
        # •
        line = re.sub(r'^\s*[-•]?\s*\d+[.)]?\s*', '', line)

        if len(line) > 10:
            questions.append(line)

    # Keep only first 5
    questions = questions[:5]

    print("\nParsed Questions:\n", questions)

    return questions


def evaluate_answer(question, answer):

    prompt = f"""
You are a senior interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate professionally.

Return in this format:

Score: X/10

Strengths

Weaknesses

Missing Concepts

Ideal Answer

Suggestions for Improvement
"""

    return llm.invoke(prompt).content