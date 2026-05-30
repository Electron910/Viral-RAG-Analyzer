from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest, chat
from dotenv import load_dotenv
import os

load_dotenv()
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass


load_dotenv()

app = FastAPI(title="Viral RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Viral RAG Backend is running on Hugging Face Spaces!"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
