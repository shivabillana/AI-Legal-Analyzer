```markdown
# 📄 AI Contract & Legal Document Analyzer

An AI-powered application that analyzes legal documents, extracts key clauses, evaluates risks, and allows users to interactively query contracts using natural language.

---

## 🚀 Features

### 📑 Document Processing
- Upload PDF or DOCX contracts
- Automatic text extraction and chunking
- Semantic embedding using Sentence Transformers

### 🧠 Clause Intelligence
- Clause classification (Termination, Liability, Payment, Confidentiality)
- Metadata tagging for each chunk

### ⚠️ Risk Analysis
- AI-based risk scoring (1–10)
- Explanation of risks
- "Explain Like I’m 5" (ELI5) simplified explanations

### 🔍 Retrieval-Augmented Generation (RAG)
- Context-aware answers using ChromaDB vector database
- Semantic search over contract content

### 📌 Explainable AI
- Clause-level citations using unique IDs
- Traceable outputs for transparency

### 💬 Chat Interface
- Chat with your document
- Multi-turn Q&A
- Context-aware responses

### 📄 Smart Summary
- Automatically generates:
  - Key points
  - Important clauses
  - Risks

### 🧩 Session Management
- Unique session-based collections
- Automatic cleanup with "End Session"

---

## 🏗️ Architecture

```

Upload Document
↓
Text Extraction
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
ChromaDB (Vector Storage)
↓
-

| Classification Layer          |
| - Clause Type Detection       |
---------------------------------

```
  ↓
```

Retrieval (RAG)
↓
LLM (OpenRouter)
↓

* Risk Score
* Explanation
* ELI5
* Citations
  ↓
  Streamlit UI

```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** OpenRouter (via LangChain)
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector DB:** ChromaDB Cloud
- **Document Parsing:** LangChain Loaders

---

## 📂 Project Structure

```

├── app.py
├── documentloader.py
├── chunking.py
├── embedding.py
├── vectorstorage.py
├── retrieval.py
├── classifier.py
├── llm_engine.py
├── response_parser.py
├── test.py
├── .env
└── requirements.txt

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/legal-analyzer.git
cd legal-analyzer
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Set Environment Variables

Create a `.env` file:

```env
CHROMA_DB_API_KEY=your_key
CHROMA_DB_TENANT=your_tenant
CHROMA_DB_DATABASE=your_database

MODEL_NAME=your_openrouter_model
OPENROUTER_API_KEY=your_api_key
```

---

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 💡 Usage

1. Upload a legal document (PDF/DOCX)
2. View auto-generated summary
3. Ask questions in chat
4. Get:

   * Risk score
   * Explanation
   * Simplified explanation
   * Clause citations

---

## 🔥 Key Highlights

* Semantic clause classification (no keyword matching)
* Explainable AI with citations
* Session-based vector storage
* RAG + LLM hybrid system
* Interactive chat interface

---

## 🚀 Future Enhancements

* ⚖️ Contract comparison (A vs B)
* 📊 Risk dashboard visualization
* 📄 Clickable clause highlighting
* 🧠 Memory-aware chat
* 🏢 Domain-specific fine-tuning

---

## 📜 License

MIT License

---

## 👤 Author

Shiva Kumar

---
