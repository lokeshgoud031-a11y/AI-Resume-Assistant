from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from backend.rag import process_resume, ask_question

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Resume Assistant Backend Running"
    }


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_resume(file_path)

    return {
        "message": "Resume uploaded successfully"
    }


@app.post("/ask")
async def ask_resume(request: QuestionRequest):

    answer = ask_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }