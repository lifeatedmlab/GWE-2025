# RAG Chatbot for DPR RI Legislative Documents

A clean, streamlined RAG (Retrieval-Augmented Generation) chatbot implementation for DPR RI legislative documents without unnecessary category system complexity.

## Features

- **Simple Document Processing**: Process PDF, DOCX, and TXT files without category complexity
- **Vector Search**: Fast semantic search using sentence transformers
- **Clean Interface**: User-friendly chat interface without confusing category syntax
- **Efficient Indexing**: Only essential metadata fields are indexed
- **Deduplication**: Automatic detection of already processed documents

## Why No Categories?

This implementation deliberately excludes a category system because:
- All documents are the same type (DPR RI legislative documents)
- Categories would be hard-coded to a single value ("peraturan_dewan")
- Simplifies the codebase and user experience
- Focuses on essential functionality

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the chatbot:
```bash
python rag_chatbot.py
```

## Usage

1. **Start the application**: Run `python rag_chatbot.py`
2. **Process documents**: Enter the path to your documents folder when prompted
3. **Ask questions**: Type your questions in Indonesian about the DPR RI documents
4. **Get help**: Type 'help' for usage instructions
5. **Exit**: Type 'exit', 'quit', or 'keluar' to quit

## Example Queries

- "Apa itu peraturan dewan?"
- "Bagaimana prosedur pengajuan proposal?"
- "Jelaskan tentang tata tertib DPR"

## Architecture

### DocumentProcessor Class
- Extracts text from various file formats
- Chunks text for optimal retrieval
- Creates vector embeddings using sentence transformers
- Stores in Qdrant vector database with minimal metadata

### RAGChatbot Class  
- Handles user queries and search
- Formats results without category information
- Provides clean, simple chat interface

## Metadata Structure

Clean metadata without category bloat:
```python
{
    "source": "document_name.pdf",
    "file_hash": "abc123...",
    "processed_at": "2025-01-14T...", 
    "file_path": "/path/to/file",
    "chunk_id": "hash_0",
    "chunk_index": 0,
    "text": "document content..."
}
```

## Benefits of This Approach

- **Simplified codebase**: ~50 fewer lines of category-related code
- **Better UX**: No confusing category filter syntax
- **Faster processing**: One less field to index
- **Easier maintenance**: Less complexity to maintain
- **Focused functionality**: Optimized for single document type

## File Support

- PDF files (.pdf)
- Word documents (.docx, .doc)  
- Text files (.txt)

## Technical Details

- **Vector Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Database**: Qdrant (in-memory for simplicity)
- **Chunking**: 1000 characters with 200 character overlap
- **Distance**: Cosine similarity for semantic search