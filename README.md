# Mistral Document Q&A API

A FastAPI-based document question-answering system powered by Mistral AI. Upload documents (text or PDF) and ask questions about them using natural language.

## 🎯 Demo

### Quick Start
```bash
# 1. Upload a document
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@document.pdf"

# 2. Ask a question
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?", "document_id": "document.pdf"}'
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## 🚀 Features

- **Document Upload**: Upload text files (.txt) and PDFs (.pdf)
- **AI-Powered Q&A**: Ask questions and get answers based on document content
- **PDF Support**: Automatically extracts text from PDF documents
- **RESTful Design**: Clean, well-documented API endpoints
- **Interactive Docs**: Auto-generated Swagger UI for easy testing
- **Mistral Integration**: Leverages Mistral AI's language models

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework
- **Mistral AI**: Large language model for question answering
- **PyPDF2**: PDF text extraction
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment

## 📋 Prerequisites

- Python 3.8+
- Mistral AI API key ([Get one here](https://console.mistral.ai/))

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/JoelAlumasa/mistral-doc-qa.git
cd mistral-doc-qa
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your Mistral API key:
```bash
echo "MISTRAL_API_KEY=your_api_key_here" > .env
```

## 🚀 Usage

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Interactive Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation where you can test all endpoints.

### API Endpoints

#### 1. Upload Document
```bash
POST /upload
```
Upload a text or PDF document to the system.

**Supported formats:**
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.md` - Markdown files

**Example using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "document_id": "document.pdf",
  "size": 1234,
  "file_type": "PDF",
  "message": "PDF document 'document.pdf' uploaded successfully"
}
```

#### 2. Ask Question
```bash
POST /ask
```
Ask a question about an uploaded document.

**Example using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "document_id": "document.pdf"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "What is the main topic?",
  "answer": "Based on the document, the main topic is...",
  "document_id": "document.pdf"
}
```

#### 3. List Documents
```bash
GET /documents
```
Get a list of all uploaded documents.

**Response:**
```json
{
  "count": 2,
  "documents": [
    {"id": "doc1.txt", "size": 1234},
    {"id": "report.pdf", "size": 5678}
  ]
}
```

## 🏗️ Project Structure
```
mistral-doc-qa/
├── app/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # FastAPI application and endpoints
│   └── config.py         # Configuration management
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 💡 How It Works

1. **Upload**: Documents (text or PDF) are uploaded via the `/upload` endpoint
2. **Storage**: Text is extracted and stored in memory with the filename as ID
3. **Query**: When you ask a question via `/ask`, the document content is sent to Mistral AI as context
4. **Response**: Mistral AI generates an answer based on the document content

## 🔒 Security Notes

- The `.env` file containing your API key is excluded from git via `.gitignore`
- In production, use environment variables or secret management services
- CORS is currently set to allow all origins (`["*"]`) - restrict this in production
- No authentication implemented - add auth for production use

## 🚧 Current Limitations

- Documents are stored in memory (lost on restart)
- Document content is limited to 3000 characters for AI processing
- No authentication/authorization implemented
- Single-user system (no multi-tenancy)

## 🔮 Future Improvements

- [ ] Implement persistent storage (PostgreSQL/MongoDB)
- [ ] Add user authentication and authorization
- [ ] Support multiple AI models (GPT-4, Claude, etc.)
- [ ] Add document chunking for larger files
- [ ] Implement caching for faster responses
- [ ] Add support for more file formats (DOCX, HTML, etc.)
- [ ] Document versioning and history
- [ ] Rate limiting and usage analytics
- [ ] Streaming responses for long answers
- [ ] Multi-document querying

## 🧪 Testing

Run the interactive docs to test:
```bash
uvicorn app.main:app --reload
# Visit http://127.0.0.1:8000/docs
```

## 📝 License

MIT License - feel free to use this project for learning or building upon.

## 🤝 Contributing

This is a learning project for the Mistral AI internship application. Feedback and suggestions are welcome!

## 👤 Author

**Joel Alumasa**
- GitHub: [@JoelAlumasa](https://github.com/JoelAlumasa)
- Project: [mistral-doc-qa](https://github.com/JoelAlumasa/mistral-doc-qa)

---

**Built with ❤️ for the Mistral AI Software Engineer Internship**

*Demonstrating FastAPI, AI integration, PDF processing, and clean code practices.*
