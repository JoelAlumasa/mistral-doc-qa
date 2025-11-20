from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mistralai import Mistral
import os
from pathlib import Path
from app.config import get_settings

settings = get_settings()
app = FastAPI(
    title="Mistral Document Q&A",
    description="Smart document Q&A powered by Mistral AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mistral_client = Mistral(api_key=settings.mistral_api_key)
documents = {}

class QuestionRequest(BaseModel):
    question: str
    document_id: str

@app.get("/")
async def root():
    return {
        "message": "Mistral Document Q&A API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "upload": "/upload",
            "ask": "/ask"
        }
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        doc_id = file.filename
        documents[doc_id] = text
        
        return {
            "status": "success",
            "document_id": doc_id,
            "size": len(text),
            "message": f"Document '{doc_id}' uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    if request.document_id not in documents:
        raise HTTPException(status_code=404, detail=f"Document not found")
    
    doc_content = documents[request.document_id]
    prompt = f"""Based on this document, answer the question.

Document:
{doc_content[:3000]}

Question: {request.question}

Answer:"""
    
    try:
        response = mistral_client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        
        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
            "document_id": request.document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/documents")
async def list_documents():
    return {
        "count": len(documents),
        "documents": [{"id": k, "size": len(v)} for k, v in documents.items()]
    }
