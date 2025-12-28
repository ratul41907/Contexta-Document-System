import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.query_engine import add_pdf_to_store, search_chunks
from app.rag_engine import answer_question

app = FastAPI(title="AI Document Search + Report Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported."}
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())
    return add_pdf_to_store(save_path)

@app.post("/search")
def search(payload: dict):
    q = payload.get("question", "").strip()
    if not q:
        return {"error": "Missing question."}
    return search_chunks(q, int(payload.get("k", 5)))

@app.post("/ask")
def ask(payload: dict):
    q = payload.get("question", "").strip()
    if not q:
        return {"error": "Missing question."}
    return answer_question(q, int(payload.get("k", 5)))
