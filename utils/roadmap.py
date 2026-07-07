import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0
)


def generate_roadmap(days):

    prompt = f"""
Create a placement preparation roadmap.

Duration

{days} days

Cover

DSA

DBMS

Operating System

Computer Networks

OOP

SQL

HR

Aptitude

Daily schedule.

"""

    return llm.invoke(prompt).content