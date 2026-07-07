import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0.3
)

def generate_quiz(topic, num_questions):

    prompt = f"""
Generate exactly {num_questions} multiple-choice questions on the topic "{topic}".

Return ONLY a valid JSON array.

The format MUST be:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A",
    "explanation": "Explanation of the correct answer"
  }}
]

Rules:
1. Return ONLY JSON.
2. Do NOT include markdown.
3. Do NOT include ```json.
4. Every question must have exactly four options.
5. The answer must be one of A, B, C, or D.
"""

    response = llm.invoke(prompt).content.strip()

    # Remove markdown if Groq returns it
    response = (
        response.replace("```json", "")
                .replace("```", "")
                .strip()
    )

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        # Sometimes Groq adds text before/after JSON
        start = response.find("[")
        end = response.rfind("]") + 1

        if start != -1 and end != -1:
            response = response[start:end]

        return json.loads(response)