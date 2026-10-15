from langchain_ollama import ChatOllama
import json
import re

grader = ChatOllama(
    model="llama3.2",
    temperature=0
)


def grade_answer(question, context, answer):
    prompt = f"""
Evaluate whether the answer is factually supported by the evidence.

QUESTION:
{question}

EVIDENCE:
{context}

ANSWER:
{answer}

Evaluation rules:
- Judge factual meaning, not answer length or exact wording.
- Accept faithful paraphrases and concise answers.
- If the question asks for a list, check whether all essential items are included.
- Do not require extra explanation when the answer only needs to identify or list facts.
- Mark supported=true if every essential fact in the answer is supported
  by the evidence and the answer adequately answers the question.
- Mark supported=false if the answer omits an essential part of the requested
  answer, contradicts the evidence, or includes unsupported factual claims.
- Carefully check the actual answer before claiming that any fact is missing.
- Never claim a fact is missing if it is explicitly present in the answer.
- Do not penalize correct answers merely because they are shorter than the evidence.

Return one JSON object in this exact format:
{{"supported": true, "reason": "brief explanation"}}

Use false instead of true when the answer is unsupported or incomplete.
Return valid JSON only.
"""

    response = grader.invoke(prompt)
    raw = response.content.strip()

    print("Answer grader response:", repr(raw))

    # Extract a JSON object, including when the model adds surrounding text.
    match = re.search(r"\{.*\}", raw, re.DOTALL)

    if not match:
        return {
            "supported": False,
            "reason": "The grader did not return valid JSON."
        }

    try:
        result = json.loads(match.group())

        supported = result.get("supported")

        if not isinstance(supported, bool):
            raise ValueError("The supported field must be true or false.")

        return {
            "supported": supported,
            "reason": str(
                result.get("reason", "No explanation provided.")
            )
        }

    except (json.JSONDecodeError, ValueError):
        return {
            "supported": False,
            "reason": "The grader returned an invalid result."
        }