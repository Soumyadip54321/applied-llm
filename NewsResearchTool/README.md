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

## 🧠 Key Capabilities

- 🔗 Multi-URL news ingestion  
- 📚 Retrieval-Augmented Generation (RAG)  
- 🧩 Cross-article reasoning  
- 📝 Question answering over long-form content  
- 🧠 Reduced hallucination via retrieval grounding  
- ? Tackling complex questions involving multiple lines.

---

## 🏗️ Architecture Overview

User Question
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
NewsResearchTool/
├── app.py
├── backend/
│   ├── cache
│   ├── tool_based_RAG.py
├── frontend/
│   └── app.py
│   ├── cache
└── README.md
```


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

---

## 📈 Future Enhancements

- Source citations in responses
- Streaming answers
- Speech to text conversion
- Avoid LLM hallucinations i.e. even with URLs of news landing page
  RAG agents give detailed response which actually isn't actual news, hence
  fetch URLs from landing page and then pass those to RAG.

---

## 📄 License

MIT License
