import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter

load_dotenv()

llm = ChatOpenRouter(
    model = os.getenv("MODEL_NAME"),
)


def analyze_clauses(question,context_chunks):

    context = "\n\n".join(
    [
        f"Clause ID: {chunk['id']} (Type: {chunk['clause_type']}): {chunk['text']}"
        for chunk in context_chunks
    ]
)

    prompt = f"""
    You are a legal assistant AI.

Analyze the following clauses and provide:

- clause_type
- risk_score (1-10)
- reason
- eli5 explanation
- citations (which clause numbers support your answer)

IMPORTANT:
- Use Clause IDs provided (e.g., Performance_Bond_Sample.pdf_2)
- Return ONLY valid JSON

Format:

{{
  "clause_type": "",
  "risk_score": 0,
  "reason": "",
  "eli5": "",
  "citations": [
    {{
      "clause_id": "Performance_Bond_Sample.pdf_2",
      "text": ""
    }}
  ]
}}

Context:
{context}

Question:
{question}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return {"error": str(e)}
    
def generate_summary(chunks):
    context = "\n\n".join([chunk[:1000] for chunk in chunks])

    prompt = f"""
    Summarize this document:

    - Key points
    - Important clauses
    - Any risks

    Keep it concise.

    Context:
    {context}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content