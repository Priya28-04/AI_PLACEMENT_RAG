import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0
)


def analyze_resume(resume_text):

    prompt = f"""
Analyze this resume.

Give

ATS Score

Missing Skills

Weaknesses

Strengths

Projects Improvement

Placement Readiness

Resume

{resume_text}
"""

    return llm.invoke(prompt).content