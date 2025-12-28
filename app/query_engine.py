import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.pdf_reader import extract_text_from_pdf
from app.embedder import get_collection

splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

def add_pdf_to_store(pdf_path: str) -> dict:
    text = extract_text_from_pdf(pdf_path).strip()
    if not text:
        return {"added": 0, "message": "No extractable text found."}

    chunks = splitter.split_text(text)
    filename = os.path.basename(pdf_path)

    col = get_collection()
    ids = [f"{filename}__{i}" for i in range(len(chunks))]
    metas = [{"source": filename, "chunk": i} for i in range(len(chunks))]

    col.add(documents=chunks, metadatas=metas, ids=ids)
    return {"added": len(chunks), "source": filename}

def search_chunks(question: str, k: int = 5) -> dict:
    col = get_collection()
    res = col.query(query_texts=[question], n_results=k)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    out = []
    for d, m in zip(docs, metas):
        out.append({"text": d, "meta": m})
    return {"results": out}
