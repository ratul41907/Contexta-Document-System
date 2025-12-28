from transformers import pipeline
from app.embedder import get_collection

_qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

def answer_question(question: str, k: int = 5) -> dict:
    col = get_collection()
    res = col.query(query_texts=[question], n_results=k)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    if not docs:
        return {"answer": "No relevant context found.", "sources": []}

    context = "\n\n".join(docs)
    out = _qa(question=question, context=context)

    sources = []
    for m in metas:
        sources.append({"source": m.get("source"), "chunk": m.get("chunk")})

    return {
        "answer": out.get("answer"),
        "confidence": out.get("score"),
        "sources": sources,
    }
