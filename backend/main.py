from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from pathlib import Path

# ✅ FIX: remove "backend." since we're already inside backend/
from utils.file_handler import extract_text_from_file
from utils.feedback_generator import get_feedback, chat_with_ai

# Load .env explicitly from backend folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
if not FIREWORKS_API_KEY:
    raise ValueError("FIREWORKS_API_KEY not found in environment. Please set it in backend/.env")

app = FastAPI()

# CORS: Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-powerpoint",
        "image/jpeg", "image/png"
    ]:
        return {"error": "Unsupported file type"}

    contents = await file.read()
    text = extract_text_from_file(file.filename, contents)
    feedback = get_feedback(text)

    return {"feedback": feedback}


class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = chat_with_ai(request.query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
