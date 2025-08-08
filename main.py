from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
from document_loader import load_pdf_from_file  # new function
from vectorstore import create_vector_store
from llm_evaluator import generate_answers

app = FastAPI()

TOKEN = "d00beb2e99cc85dd8aad42430e5ab20b916e5df2abd096b8401a3eac074fcd35"

class QARequest(BaseModel):
    questions: list[str]

# ✅ Load and embed PDF once at startup
print("[INFO] Loading policy PDF...")
text_chunks = load_pdf_from_file("data/Arogya Sanjeevani Policy - CIN - U10200WB1906GOI001713 1.pdf")
vectordb, retriever = create_vector_store(text_chunks)
print("[INFO] Policy PDF loaded and embeddings created.")

@app.post("/api/v1/hackrx/run")
async def run_chatbot(data: QARequest, authorization: str = Header(...)):
    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    answers = generate_answers(data.questions, retriever)
    return {"answers": answers}
