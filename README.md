---
title: Viral RAG Chatbot
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 🚀 Viral RAG Chatbot (The Optimizer)

An intelligent Retrieval-Augmented Generation (RAG) chatbot that allows you to compare, analyze, and deconstruct the success of viral YouTube and Instagram videos.

By pasting two video URLs, the system scrapes video metadata (views, likes, engagement rate) and extracts the full transcript. If a transcript is disabled or missing, the system automatically uses `yt-dlp` to download the audio track and transcribes it locally using the AI `faster-whisper` model. All of this data is vectorized and fed into Google's **Gemini 2.5 Flash**, allowing you to ask deep analytical questions about why one video performed better than another, compare hooks, and contrast structural themes.

---

## ✨ Core Features
* **Cross-Platform Analysis:** Compare YouTube vs YouTube, Instagram vs Instagram, or YouTube vs Instagram seamlessly.
* **Rich Metadata Injection:** Context-aware LLM that factors in follower counts, views, likes, and engagement rates into its analysis.
* **Fallback AI Transcription:** If a video has no captions, the system uses OpenAI's Whisper model to transcribe the audio locally on your machine.
* **Modern UI:** Built with React, Vite, and Lucide React, featuring real-time Markdown rendering for chat responses.
* **Semantic Search:** Uses HuggingFace BGE embeddings and ChromaDB to instantly retrieve the most relevant moments from a video's transcript based on your chat queries.

---

## 🛠️ Tech Stack

**Frontend:**
- **React 19** & **Vite**: For a lightning-fast, modern component architecture.
- **Lucide React**: Clean, consistent iconography.
- **React Markdown**: Renders the AI's complex analytical responses beautifully.

**Backend:**
- **FastAPI** & **Uvicorn**: High-performance asynchronous Python web framework.
- **LangChain**: Orchestrates the RAG pipeline, chaining prompts, retrievers, and LLMs.
- **ChromaDB**: Local vector database for incredibly fast semantic search.
- **Google Generative AI (Gemini 2.5 Flash)**: The core intelligence powering the chatbot's analysis.

**Data Pipelines & Processing:**
- **yt-dlp** & **FFmpeg**: Extracts pure audio from restricted or uncaptioned videos.
- **faster-whisper**: On-device transcription of downloaded audio tracks.
- **youtube-transcript-api**: Rapid scraping of existing YouTube captions.

---

## 📂 Project Structure

```text
the-optimizer/
│
├── frontend/                   # React + Vite Application
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── api/                # Axios API client setup (client.js)
│   │   ├── components/         # React Components (ChatPanel, VideoCard, UrlInput)
│   │   ├── App.jsx             # Main Application Layout
│   │   ├── App.css             # UI Styling & Layout
│   │   └── main.jsx            # React Entry Point
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
│
├── backend/                    # FastAPI Server
│   ├── chains/                 # Langchain memory & custom chains
│   ├── models/                 # Pydantic data models (ChatRequest, etc.)
│   ├── routers/                # API Endpoints (/chat, /ingest)
│   ├── services/               # Core logic (youtube_service, vectorstore)
│   ├── utils/                  # Helpers (chunker, session management)
│   ├── main.py                 # FastAPI Entry Point
│   └── requirements.txt        # Backend dependencies
│
└── README.md                   # You are here!
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:
1. **Node.js** (v18+)
2. **Python** (3.10+)
3. **FFmpeg** (Required for local Whisper transcription). 
   - *Windows Users:* Install via PowerShell using `winget install ffmpeg`. **Crucial:** You must add the FFmpeg binary folder to your system's `PATH` Environment Variables and restart your terminal.
4. **Google Gemini API Key**

---

## 💻 Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd the-optimizer
```

### 2. Backend Setup
Navigate to the backend directory, create a virtual environment, and install the dependencies:
```bash
cd backend
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install dependencies:
```bash
cd frontend
npm install
```

---

## 🏃‍♂️ Running the Application

You will need two terminal windows running simultaneously.

**Terminal 1 (Backend Server):**
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```
*The backend will start at `http://127.0.0.1:8000`*

**Terminal 2 (Frontend Server):**
```bash
cd frontend
npm run dev
```
*The frontend will start at `http://localhost:5173`*

---

## 🧠 How it Works Under the Hood
1. **Data Ingestion (`/ingest`):** When you click "Analyze", the FastAPI backend fetches the metadata for both videos. It attempts to download YouTube transcripts directly. If a transcript doesn't exist, it uses `yt-dlp` to rip the audio and feeds it through `faster-whisper` for an on-the-fly local transcription.
2. **Chunking & Vectorization:** The transcripts are broken into digestible chunks using Langchain's text splitters. These chunks are enriched with the creator's metadata (so the LLM never loses context of the stats), embedded using HuggingFace BGE embeddings, and stored in a local ChromaDB vector database.
3. **Conversational Retrieval (`/chat`):** When you ask a question, the system searches ChromaDB for the top most relevant transcript chunks, combines them with the video metadata and your previous chat history, and streams a highly analytical response from **Gemini 2.5 Flash** back to the React frontend in real-time.
