from sentence_transformers import util

def init_classifier(model):
    clause_examples = {
            "termination": "Ending or canceling a contract",
            "liability": "Responsibility for damages or legal issues",
            "payment": "Salary, fees, or payment terms",
            "confidentiality": "Keeping information secret or private"
        }

    example_embeddings = {
            label: model.encode(text, convert_to_tensor=True)
            for label, text in clause_examples.items()
        }
    return example_embeddings

def classify_clause(clause_text, model, example_embeddings):
    text_embedding = model.encode(clause_text, convert_to_tensor=True)

    best_score = -1
    best_label = "other"

    for label,emb in example_embeddings.items():
        score = util.cos_sim(text_embedding, emb).item()

        if score > best_score:
            best_score = score
            best_label = label
        
    if best_score < 0.3:
        return "other"
        
    return best_label
