from documentloader import fileloader
from chunking import dividingchunks
from embedding import generate_embeddings
from sentence_transformers import SentenceTransformer
from vectorstorage import create_collection, store_chunks
from retrieval import query_collection
from classifier import classify_clause,init_classifer
from llm_engine import analyze_clauses
from response_parser import parse_llm_response, format_for_ui

model = SentenceTransformer('all-MiniLM-L6-v2') # Example model, replace with your choice

file = "Performance_Bond_Sample.pdf"
example_embeddings = init_classifer(model)
documents = fileloader(file)
chunks = dividingchunks(documents)
embedding = generate_embeddings(chunks,model) # Assuming 'model' is defined elsewhere


print("Documents:",len(documents))
print("Chunks:",len(chunks))
print("Embeddings:",len(embedding))


collection_name = "test_collection"
collection = create_collection(collection_name)
store_chunks(collection,chunks,embedding,model,example_embeddings)

query = "What is bond breaking amount?"
results = query_collection(collection,query,model)
retrieved_ids = results["ids"][0]
retrieved_docs = results['documents'][0]
retrieved_metadatas = results['metadatas'][0]
    
context_chunks = [
    {
        "id": cid,
        "text": doc,
        "clause_type": meta.get("clause_type", "unknown")
    }
    for cid,doc, meta in zip(retrieved_ids, retrieved_docs, retrieved_metadatas)
]

analysis = analyze_clauses(query, context_chunks)

parsed = parse_llm_response(analysis)

ui_data = format_for_ui(parsed)

print("Parsed LLM Response:", parsed)


