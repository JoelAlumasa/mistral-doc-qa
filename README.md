cd ~/projects/mistral-doc-qa

cat > README.md << 'EOF'
# Mistral Document Q&A API

A FastAPI-based document question-answering system powered by Mistral AI. Upload documents and ask questions about them using natural language.

## 🚀 Features

- **Document Upload**: Upload text documents via REST API
- **AI-Powered Q&A**: Ask questions and get answers based on document content
- **RESTful Design**: Clean, well-documented API endpoints
- **Interactive Docs**: Auto-generated Swagger UI for easy testing
- **Mistral Integration**: Leverages Mistral AI's language models

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework
- **Mistral AI**: Large language model for question answering
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
Upload a text document to the system.

**Example using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.txt"
```

**Response:**
```json
{
  "status": "success",
  "document_id": "document.txt",
  "size": 1234,
  "message": "Document 'document.txt' uploaded successfully"
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
    "document_id": "document.txt"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "What is the main topic?",
  "answer": "Based on the document, the main topic is...",
  "document_id": "document.txt"
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
    {"id": "doc2.txt", "size": 5678}
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

## 🔒 Security Notes

- The `.env` file containing your API key is excluded from git via `.gitignore`
- In production, consider using environment variables or secret management services
- CORS is currently set to allow all origins (`["*"]`) - restrict this in production

## 🚧 Current Limitations

- Documents are stored in memory (lost on restart)
- Only supports plain text files (UTF-8 encoded)
- Document content is limited to 3000 characters for AI processing

## 🔮 Future Improvements

- [ ] Add PDF support
- [ ] Implement persistent storage (database)
- [ ] Add authentication
- [ ] Support multiple AI models
- [ ] Add document chunking for larger files
- [ ] Implement caching for faster responses

## 📝 License

MIT License - feel free to use this project for learning or building upon.

## 🤝 Contributing

This is a learning project for the Mistral AI internship application. Feedback and suggestions are welcome!

## 👤 Author

Joel Alumasa - [GitHub](https://github.com/JoelAlumasa)

---

**Built with ❤️ for the Mistral AI Software Engineer Internship**
EOF