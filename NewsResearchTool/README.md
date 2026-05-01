# NewsResearchTool – LLM-Powered News Research Agent (RAG)

An LLM-based research agent that answers user questions by **retrieving, analyzing, and reasoning over multiple news article URLs** using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🔍 Problem Statement

News analysis often requires reading multiple articles from different sources, comparing viewpoints, and extracting key insights — a slow and error-prone manual process.

Traditional LLMs struggle with:
- Long articles
- Multiple URLs
- Source attribution
- Hallucinations

---

## 💡 Solution

**NewsResearchTool** enables users to ask questions directly over a list of news URLs.

The agent:
1. Fetches and cleans article content from provided URLs  
2. Chunks and embeds the content  
3. Retrieves relevant passages using semantic search  
4. Uses an LLM to generate grounded, source-aware answers  
5. Answers complex questions.

This ensures **accurate, explainable, and context-aware responses**.

---

🧠 Key Capabilities
- 🔗 Multi-URL news ingestion
- 📚 Retrieval-Augmented Generation (RAG) for grounded responses
- 🧩 Cross-article reasoning across multiple news sources
- 📝 Question answering over long-form content
- 🛡️ Reduced hallucinations via retrieval-based grounding
- 🧠 Complex question handling spanning multiple narratives
- 🎙️➡️📝 Voice-to-text question input with automatic transcription
- 🔁 Fail-safe speech transcription
     - 🥇 AssemblyAI as the primary STT engine
     - 🥈 Whisper as a robust fallback

---

## 🏗️ Architecture Overview

User Question (either typed or voice recorded)
→
News URLs → Content Extraction → Chunking → Cached Embeddings
→
Vector Store
→
Relevant Context
→
LLM Generation
→
Answer


---

## 📌 Example Use Cases

- “What are different viewpoints on the recent interest rate decision?”
- “Summarize the key points across these articles.”
- “What risks are mentioned by analysts in these reports?”
- “Compare how different sources cover the same event.”

---

## 🛠️ Tech Stack

- **Language**: Python  
- **LLM**: API-based LLM (configurable)  
- **Retrieval**: Vector embeddings + similarity search  
- **Parsing**: Web scraping / article extraction  
- **Design Pattern**: Retrieval-Augmented Generation (RAG)

---

## 📂 Project Structure

```text
Root
├──NewsResearchTool/
    ├── app.py
    ├── backend/
    │   ├── tool_based_RAG.py
    |   ├── speech_to_text.py
    ├── frontend/
    │   └── app.py
    │   ├── cache
    └── README.md
```
---

## ⚙️ Installation & Setup

- **Create and activate virtual environment**
  - 
      python -m venv .venv
      source .venv/bin/activate   # macOS / Linux
      .venv\Scripts\activate      # Windows
- **Install Dependencies**
  - 
      pip install -r requirements.txt
- **Configure Environment Variables**
  -
  
      OPENAI_API_KEY=your_llm_api_key
      DB_USER=your_db_user
      DB_PASSWORD=your_db_password
      DB_HOST=localhost
      DB_PORT=3306
      DB_NAME=atliq_tshirts

- **Run the application from the project root**
  - 
      python -m streamlit run NewsResearchTool/frontend/app.py
---

## 🚀 How It Works (High Level)

1. User provides:
   - One or more news article URLs
   - A natural language question
2. Articles are fetched, cleaned, and split into chunks
3. Relevant chunks are retrieved using embeddings
4. LLM generates a grounded answer using retrieved context

---

## 🎯 Why This Project Matters

This project demonstrates:
- Practical use of **RAG for real-world information retrieval**
- Handling **unstructured data at scale**
- Designing systems that minimize hallucinations
- Applying LLMs beyond simple chat use cases
- Using dual failsafe speech-to-text models to transcribe audio.

---

## 📈 Future Enhancements

- Mitigate LLM hallucinations with news headings and short description present on news landing pages.
- Use OCR to scan newspapers and answer user queriesh as `What's on sports today?`, `What about politics?` etc.

---

## 📄 License

MIT License
