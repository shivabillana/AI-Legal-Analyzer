import chromadb
import os
from dotenv import load_dotenv
from classifier import classify_clause

load_dotenv()


client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_DB_API_KEY"),
    tenant=os.getenv("CHROMA_DB_TENANT"),
    database=os.getenv("CHROMA_DB_DATABASE")
)

def create_collection(collection_name):
    collection = client.get_or_create_collection(
        name= collection_name
    )

    return collection

def store_chunks(collection,documents,embeddings,model,example_embeddings):

    if len(documents) != len(embeddings):
        raise ValueError("The number of documents and embeddings must be the same.")
    
    ids = [
        f"{doc.metadata.get('source', 'doc')}_{i}"
        for i, doc in enumerate(documents)
    ]

    collection.add(
        ids=ids,
        documents=[chunk.page_content for chunk in documents],
        embeddings=embeddings,
        metadatas=[
            {**doc.metadata, 
             "clause_type": classify_clause(doc.page_content, model, example_embeddings)}
            for doc in documents]
    )

def delete_session_collection(session_id):
    try:
        client.delete_collection(name=session_id)
    except Exception as e:
        print(f"Error deleting collection: {e}")