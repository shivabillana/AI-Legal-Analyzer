import json

def get_risk_level(score):
    if score <= 3:
        return "LOW"
    elif score <= 6:
        return "MEDIUM"
    else:
        return "HIGH"


def parse_llm_response(response_text):
    try:
        data = json.loads(response_text)

        score = data.get("risk_score", 0)

        return {
            "clause_type": data.get("clause_type"),
            "risk_score": score,
            "risk_level": get_risk_level(score),
            "reason": data.get("reason"),
            "eli5": data.get("eli5"),
            "citations": data.get("citations", [])
        }

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON from LLM",
            "raw": response_text
        }


def format_for_ui(data):
    return {
        "summary": f"Risk Level: {data['risk_level']} ({data['risk_score']}/10)",
        "explanation": data["reason"],
        "simple_explanation": data["eli5"],
        "citations": data["citations"]
    }