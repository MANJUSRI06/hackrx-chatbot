from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
import requests
import os
from document_loader import load_pdf_from_url
from vectorstore import create_vector_store, retrieve_relevant_chunks
from llm_evaluator import generate_answers

app = FastAPI()

TOKEN = "d00beb2e99cc85dd8aad42430e5ab20b916e5df2abd096b8401a3eac074fcd35"

class QARequest(BaseModel):
    documents: str
    questions: list[str]

@app.post("/api/v1/hackrx/run")
async def run_chatbot(data: QARequest, authorization: str = Header(...)):
    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    text_chunks = load_pdf_from_url(data.documents)
    vectordb, retriever = create_vector_store(text_chunks)
    answers = generate_answers(data.questions, retriever)

    return {"answers": answers}
