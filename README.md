# ClipSense — YouTube Video Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6719?style=flat&logo=databricks&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-blue?style=flat)

> **Stop watching. Start querying.**

**ClipSense** transforms any YouTube video into a searchable knowledge base. Powered by a localized RAG pipeline, it fetches and indexes video transcripts so you can ask natural language questions and get precise, grounded answers — complete with timestamp citations pointing back to the exact moment in the video.

> No cloud storage. No manual note-taking. Just paste a URL and ask.

---

## Features

| | Feature | Description |
|:---:|:---|:---|
| 🔗 | **Automated Ingestion** | Paste a YouTube URL - transcript is fetched, sanitized, and indexed automatically |
| 💬 | **Natural Language Querying** | Ask anything about the video in plain English |
| 🕐 | **Timestamp Citations** | Every answer references exactly where in the video the information came from |
| 💾 | **Persistent Storage** | Ingest once, query many times - ChromaDB persists locally between sessions |
| ✅ | **Validation Harness** | Checks AI-generated summaries against manual ground truth for factual consistency |
| 🖥️ | **Streamlit UI** | Simple browser-based interface, no frontend experience needed |

---

## How It Works

1. 🔗 **Fetch** — YouTube Transcript API pulls the transcript from the video URL
2. 🧹 **Sanitize** — noise like `[Music]` and `[Applause]` is stripped from the text
3. ✂️ **Chunk** — transcript is split into overlapping segments using LangChain's text splitter
4. 🔢 **Embed** — each chunk is embedded with OpenAI `text-embedding-3-small`
5. 💾 **Store** — embeddings are stored locally in ChromaDB with `video_id` and timestamp metadata
6. 💬 **Query** — user question is embedded, top-k chunks retrieved, GPT-4o generates a grounded answer

---

## Project Structure

```
Clipsense-YouTube-Video-Intelligence/
│
├── source/
│   ├── app.py                  # Streamlit web app
│   ├── ingestion_pipeline.py   # Transcript ingestion pipeline
│   ├── llm_validation.py       # Validation harness
│   └── db/
│       └── chroma_db/          # Local vector store (auto-created)
│
├── requirements.txt            # Dependencies
└── .env                        # Environment variables
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/ameyakonk/Clipsense-YouTube-Video-Intelligence.git
cd Clipsense-YouTube-Video-Intelligence
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure your API key**
```bash
cp .env.example .env
```
Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=sk-...
```

**5. Run the app**
```bash
streamlit run source/app.py
```

Open **http://localhost:8501** in your browser.

---

## Usage

```
┌─────────────────────────────────────────┐
│  🔗  Paste a YouTube URL                │
│      any video with captions            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  💬  Ask a question                     │
│      "What did the speaker say about X?"│
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  ⚙️   ClipSense processes               │
│      Ingests on first run (~10 sec)     │
│      Instant on subsequent queries      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  ✅  Get your answer                    │
│      With timestamp citations           │
└─────────────────────────────────────────┘
```

---

## Validation Harness

The validation harness checks factual consistency of AI-generated summaries against manual ground truth timestamps.

```bash
python source/llm_validation.py
```

Ground truth is defined in `ground_truth.json`:

```json
[
  {
    "timestamp_range": [90, 150],
    "question": "What does the speaker say about X?",
    "expected_keywords": ["keyword1", "keyword2"]
  }
]
```

The harness extracts transcript text for each timestamp range, generates a summary, and checks if expected keywords appear — reporting a consistency score per case.

---

## Tech Stack

| Component | Technology |
|:---|:---|
| Transcript Fetching | [![YouTube](https://img.shields.io/badge/YouTube_Transcript_API-FF0000?style=flat&logo=youtube&logoColor=white)](https://github.com/jdepoix/youtube-transcript-api) |
| Embeddings | [![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)](https://platform.openai.com/docs/guides/embeddings) |
| Vector Store | [![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6719?style=flat&logo=databricks&logoColor=white)](https://www.trychroma.com) |
| LLM | [![GPT-4o](https://img.shields.io/badge/GPT--4o-412991?style=flat&logo=openai&logoColor=white)](https://platform.openai.com/docs/models/gpt-4o) |
| RAG Framework | [![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com) |
| UI | [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io) |

---

## Author

**Ameya Konkar** — [LinkedIn](https://linkedin.com/in/ameyakonkar) · [GitHub](https://github.com/ameyakonk)
