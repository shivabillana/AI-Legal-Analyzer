import streamlit as st
import uuid
import os

from documentloader import fileloader
from chunking import dividingchunks
from embedding import generate_embeddings
from sentence_transformers import SentenceTransformer
from vectorstorage import create_collection, store_chunks, delete_session_collection
from retrieval import query_collection
from classifier import init_classifier
from llm_engine import analyze_clauses, generate_summary
from response_parser import parse_llm_response, format_for_ui


st.set_page_config(page_title="AI Legal Analyzer", layout="wide")
st.title("📄 AI Contract & Legal Document Analyzer")

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4()}"

if "summary" not in st.session_state:
    st.session_state.summary = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "collection_created" not in st.session_state:
    st.session_state.collection_created = False

session_id = st.session_state.session_id


st.sidebar.write("🟢 Session Active")


if st.sidebar.button("🛑 End Session"):
    delete_session_collection(session_id)
    st.session_state.clear()
    st.success("Session ended. Data cleared.")
    st.stop()


uploaded_file = st.file_uploader("Upload Contract", type=["pdf", "docx"])

model = SentenceTransformer('all-MiniLM-L6-v2') # Example model, replace with your choice

example_embeddings = init_classifier(model)


if uploaded_file :

    temp_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    documents = fileloader(temp_path)
    chunks = dividingchunks(documents)
    embeddings = generate_embeddings(chunks,model) # Assuming 'model' is defined elsewhere

    if not st.session_state.collection_created:
        collection_name = session_id
        collection = create_collection(collection_name)
        store_chunks(collection,chunks,embeddings,model,example_embeddings)
        st.session_state.collection = collection
        st.session_state.collection_created = True

    if st.session_state.summary is None:
        query = "Important points, key clauses, and risks in this document"
        top_k = 5
        results = query_collection(st.session_state.collection,query,model, top_k)
        retrieved_docs = results["documents"][0]

        st.session_state.summary = generate_summary(retrieved_docs)

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("📄 Document Summary")

    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.info("Upload a document to see the summary here.")


with col2:
    st.subheader("💬 Chat with Document")

    user_query = st.text_input("Enter your question about the document:")

    if user_query:
        results = query_collection(st.session_state.collection, user_query, model)
        retrieved_docs = results["documents"][0]
        retrieved_metadata = results["metadatas"][0]
        retrieved_ids = results["ids"][0]

        context_chunks = [
            {
                "id": cid,
                "text": doc,
                "clause_type": meta.get("clause_type", "unknown")
            }
            for cid, doc, meta in zip(
                retrieved_ids,
                retrieved_docs,
                retrieved_metadata
            )
        ]


        llm_response = analyze_clauses(user_query, context_chunks)

        parsed_response = parse_llm_response(llm_response)

        formatted_response = format_for_ui(parsed_response)

        st.session_state.chat_history.append((user_query, formatted_response))

    for q,a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            summary_text = a.get("summary","")

        # 🎨 Risk coloring
            if "HIGH" in summary_text:
                st.error(summary_text)
            elif "MEDIUM" in summary_text:
                st.warning(summary_text)
            else:
                st.success(summary_text)

            st.write("**Explanation:**", a["explanation"])
            st.write("**Simple Explanation:**", a["simple_explanation"])

            if a["citations"]:
                st.write("📌 Citations:")
                for c in a["citations"]:
                    st.write(f"- {c.get('clause_id', 'N/A')}") 

