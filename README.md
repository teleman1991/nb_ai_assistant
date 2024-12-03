# Workplace Document AI Assistant

An intelligent document processing and analysis tool designed for modern workplaces. This FastAPI application provides powerful document analysis capabilities including summarization, key point extraction, and natural language querying.

## Features

- **Multi-Format Support**
  - PDF document processing
  - DOCX file handling
  - Plain text analysis
  
- **Advanced Document Analysis**
  - Automatic text extraction
  - Document summarization
  - Key points identification
  - Metadata extraction

- **Natural Language Querying**
  - Context-aware responses
  - Intelligent question answering
  - Document-based reasoning

## Installation

### Prerequisites
1. Python 3.8 or higher
2. pip package manager

### Setup
1. Clone this repository:
```bash
git clone https://github.com/teleman1991/nb_ai_assistant.git
cd nb_ai_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server
1. Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage

### Process Document
```python
import requests

# Process a document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/process/',
        files={'file': f}
    )
    results = response.json()
    print(results['summary'])
```

### Query Document
```python
# Query a document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/query/',
        files={'file': f},
        data={'query': 'What are the main conclusions?'}
    )
    answer = response.json()['answer']
    print(answer)
```

## API Endpoints

- `POST /process/`
  - Process a document and get summary, key points, and metadata
  - Accepts PDF, DOCX, or TXT files
  
- `POST /query/`
  - Ask specific questions about a document
  - Returns context-aware answers

## Security

- API key authentication required for all endpoints
- Secure file handling and processing
- Rate limiting implemented

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.