"""
Mistral Document Q&A API

A FastAPI-based service that allows users to upload documents and ask questions
about them using Mistral AI's language models.

Key Features:
- Document upload (text files and PDFs)
- AI-powered question answering
- RESTful API design
- Interactive API documentation
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mistralai import Mistral
import os
from pathlib import Path
from app.config import get_settings
import PyPDF2
import io

# Load configuration from .env file
settings = get_settings()

# Initialize FastAPI application
app = FastAPI(
    title="Mistral Document Q&A",
    description="Smart document Q&A powered by Mistral AI",
    version="1.0.0"
)

# Enable CORS to allow frontend applications to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Mistral AI client with API key
mistral_client = Mistral(api_key=settings.mistral_api_key)

# In-memory storage for uploaded documents
# Key: document filename, Value: document text content
# Note: In production, use a database for persistence
documents = {}


class QuestionRequest(BaseModel):
    """
    Request model for asking questions about documents.
    
    Attributes:
        question (str): The question to ask about the document
        document_id (str): The ID/filename of the document to query
    """
    question: str
    document_id: str


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_content (bytes): PDF file content as bytes
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        Exception: If PDF cannot be parsed
    """
    try:
        # Create a PDF reader object from bytes
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


@app.get("/")
async def root():
    """
    Root endpoint providing API information and available endpoints.
    
    Returns:
        dict: Welcome message and available API endpoints
    """
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
    """
    Upload a document (text or PDF) to the system.
    
    Supports:
    - Plain text files (.txt)
    - PDF files (.pdf)
    
    The document is stored in memory and can be queried using the /ask endpoint.
    
    Args:
        file (UploadFile): The file to upload
        
    Returns:
        dict: Upload status, document ID, file size, and file type
        
    Raises:
        HTTPException: If file cannot be processed
    """
    try:
        # Read file contents
        content = await file.read()
        
        # Determine file type and extract text accordingly
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension == '.pdf':
            # Extract text from PDF
            text = extract_text_from_pdf(content)
            file_type = "PDF"
        elif file_extension in ['.txt', '.md']:
            # Decode text file
            text = content.decode('utf-8')
            file_type = "Text"
        else:
            # Try to decode as text, fallback to error
            try:
                text = content.decode('utf-8')
                file_type = "Text"
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_extension}. Please upload .txt or .pdf files."
                )
        
        # Store document using filename as ID
        doc_id = file.filename
        documents[doc_id] = text

        return {
            "status": "success",
            "document_id": doc_id,
            "size": len(text),
            "file_type": file_type,
            "message": f"{file_type} document '{doc_id}' uploaded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error processing file: {str(e)}"
        )


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question about an uploaded document using Mistral AI.
    
    The document content is provided as context to the AI model,
    which then generates an answer based on the document.
    
    Args:
        request (QuestionRequest): Question and document ID
        
    Returns:
        dict: The AI-generated answer along with metadata
        
    Raises:
        HTTPException: If document not found or AI request fails
    """
    # Verify document exists
    if request.document_id not in documents:
        raise HTTPException(
            status_code=404, 
            detail=f"Document '{request.document_id}' not found. Please upload it first."
        )

    # Retrieve document content
    doc_content = documents[request.document_id]
    
    # Construct prompt with document context and question
    # Limit document to first 3000 characters to stay within token limits
    prompt = f"""Based on this document, answer the question.

Document:
{doc_content[:3000]}

Question: {request.question}

Answer:"""

    try:
        # Call Mistral AI API
        response = mistral_client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract answer from response
        answer = response.choices[0].message.content

        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
            "document_id": request.document_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error calling Mistral API: {str(e)}"
        )


@app.get("/documents")
async def list_documents():
    """
    List all currently uploaded documents.
    
    Returns:
        dict: Count and list of all documents with their IDs and sizes
    """
    return {
        "count": len(documents),
        "documents": [
            {"id": doc_id, "size": len(content)} 
            for doc_id, content in documents.items()
        ]
    }
