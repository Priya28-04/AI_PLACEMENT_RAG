import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 4})

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0
)


def ask_question(question, topic="All"):

    docs = retriever.invoke(question)

    if topic != "All":
        docs = [
            d for d in docs
            if d.metadata.get("subject") == topic
        ]

    context = "\n\n".join(
        d.page_content for d in docs
    )

    prompt = f"""
You are an expert AI Placement Preparation Assistant.

Use ONLY the given context.

Context:
{context}

Question:
{question}

Give a detailed interview-ready answer.
"""

    answer = llm.invoke(prompt)

    return answer.content, docs