"""
RAG Chatbot for DPR RI Legislative Documents
Clean implementation without category system - all documents are the same type.
"""

import os
import hashlib
import uuid
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
from datetime import datetime

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType
    from sentence_transformers import SentenceTransformer
    import PyPDF2
    import docx
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install: pip install qdrant-client sentence-transformers PyPDF2 python-docx")
    exit(1)


class DocumentProcessor:
    """Processes documents for the RAG system without category complexity."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.client = QdrantClient(":memory:")  # In-memory for simplicity
        self.collection_name = "dpr_documents"
        self._setup_collection()
        
    def _setup_collection(self):
        """Initialize the vector collection with essential indexes only."""
        try:
            # Create collection with appropriate vector settings
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            
            # Create only essential indexes
            index_fields = [
                ("file_hash", PayloadSchemaType.KEYWORD),
                ("source", PayloadSchemaType.KEYWORD),
                ("chunk_id", PayloadSchemaType.KEYWORD),
            ]
            
            for field_name, field_type in index_fields:
                try:
                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name=field_name,
                        field_schema=field_type
                    )
                except Exception as e:
                    logging.warning(f"Index for {field_name} might already exist: {e}")
                    
        except Exception as e:
            logging.error(f"Failed to setup collection: {e}")
            raise
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats."""
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                return self._extract_from_docx(file_path)
            elif file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logging.warning(f"Unsupported file format: {file_ext}")
                return ""
        except Exception as e:
            logging.error(f"Error extracting text from {file_path}: {e}")
            return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                if break_point > start + chunk_size // 2:
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
        return [chunk for chunk in chunks if chunk.strip()]
    
    def process_document(self, file_path: str, metadata: Optional[Dict] = None) -> bool:
        """Process a single document for the RAG system."""
        try:
            # Calculate file hash for deduplication
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # Check if already processed
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter={"must": [{"key": "file_hash", "match": {"value": file_hash}}]},
                limit=1
            )
            
            if search_result[0]:
                logging.info(f"Document {file_path} already processed (hash: {file_hash})")
                return True
            
            # Extract text
            text = self._extract_text_from_file(file_path)
            if not text.strip():
                logging.warning(f"No text extracted from {file_path}")
                return False
            
            # Create base metadata (clean structure)
            base_metadata = {
                "source": os.path.basename(file_path),
                "file_hash": file_hash,
                "processed_at": datetime.now().isoformat(),
                "file_path": str(file_path),
            }
            
            # Add custom metadata if provided
            if metadata:
                base_metadata.update(metadata)
            
            # Chunk the text
            chunks = self._chunk_text(text)
            logging.info(f"Processing {len(chunks)} chunks from {file_path}")
            
            # Process each chunk
            points = []
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                # Generate embedding
                embedding = self.model.encode(chunk).tolist()
                
                # Create chunk metadata
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    "chunk_id": f"{file_hash}_{i}",
                    "chunk_index": i,
                    "text": chunk,
                })
                
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=chunk_metadata
                )
                points.append(point)
            
            # Insert into collection
            if points:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logging.info(f"Successfully processed {file_path}: {len(points)} chunks indexed")
                return True
            else:
                logging.warning(f"No valid chunks created for {file_path}")
                return False
                
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            return False
    
    def process_multiple_documents(self, folder_path: str, file_pattern: str = "*", 
                                 recursive: bool = True) -> Dict[str, int]:
        """Process multiple documents in a folder."""
        results = {"success": 0, "failed": 0, "total": 0}
        
        folder = Path(folder_path)
        if not folder.exists():
            logging.error(f"Folder does not exist: {folder_path}")
            return results
        
        # Find files to process
        if recursive:
            files = list(folder.rglob(file_pattern))
        else:
            files = list(folder.glob(file_pattern))
        
        # Filter for supported file types
        supported_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        files = [f for f in files if f.suffix.lower() in supported_extensions]
        
        results["total"] = len(files)
        logging.info(f"Found {len(files)} documents to process in {folder_path}")
        
        for file_path in files:
            if self.process_document(str(file_path)):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        logging.info(f"Processing complete: {results['success']} success, {results['failed']} failed")
        return results


class RAGChatbot:
    """RAG chatbot for DPR RI documents with clean, simple interface."""
    
    def __init__(self, processor: DocumentProcessor):
        self.processor = processor
        self.client = processor.client
        self.model = processor.model
        self.collection_name = processor.collection_name
    
    def search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """Search documents using semantic similarity."""
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query).tolist()
            
            # Search in vector database
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            
            # Format results
            results = []
            for hit in search_result:
                result = {
                    "score": hit.score,
                    "text": hit.payload.get("text", ""),
                    "source": hit.payload.get("source", "unknown"),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logging.error(f"Error searching documents: {e}")
            return []
    
    def _format_context(self, search_results: List[Dict]) -> str:
        """Format search results as context for response generation."""
        if not search_results:
            return "Tidak ada dokumen yang relevan ditemukan."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            source = result.get("source", "unknown")
            text = result.get("text", "").strip()
            score = result.get("score", 0)
            
            context_parts.append(f"""
Dokumen {i}: {source} (relevansi: {score:.3f})
{text}
---""")
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response based on query and context."""
        # Simple response generation (can be enhanced with LLM)
        if not context or "Tidak ada dokumen" in context:
            return "Maaf, saya tidak menemukan informasi yang relevan dengan pertanyaan Anda dalam dokumen DPR RI yang tersedia."
        
        response = f"""Berdasarkan dokumen DPR RI yang tersedia:

{context}

Informasi di atas merupakan konten yang relevan dengan pertanyaan Anda. Silakan tinjau dokumen-dokumen tersebut untuk mendapatkan informasi lengkap."""
        
        return response
    
    def chat_loop(self):
        """Main chat interface with simple, clean user experience."""
        print("=" * 60)
        print("RAG Chatbot - DPR RI Legislative Documents")
        print("=" * 60)
        print("Ketik pertanyaan Anda tentang dokumen DPR RI.")
        print("Ketik 'exit', 'quit', atau 'keluar' untuk mengakhiri.")
        print("Ketik 'help' untuk bantuan.")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\nPertanyaan: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'keluar']:
                    print("Terima kasih! Sampai jumpa!")
                    break
                
                # Show help
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Process the query directly
                print("\nMencari dokumen yang relevan...")
                search_results = self.search_documents(user_input)
                
                if not search_results:
                    print("Maaf, tidak ada dokumen yang relevan ditemukan.")
                    continue
                
                # Format context and generate response
                context = self._format_context(search_results)
                response = self.generate_response(user_input, context)
                
                print(f"\nJawaban:")
                print(response)
                
            except KeyboardInterrupt:
                print("\n\nTerima kasih! Sampai jumpa!")
                break
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                logging.error(f"Error in chat loop: {e}")
    
    def _show_help(self):
        """Show help text with simple, clear instructions."""
        print("""
BANTUAN - RAG Chatbot DPR RI

Cara menggunakan:
• Ketik pertanyaan Anda dalam bahasa Indonesia
• Contoh: "Apa itu peraturan dewan?"
• Contoh: "Bagaimana prosedur pengajuan proposal?"

Perintah khusus:
• 'help' - Menampilkan bantuan ini
• 'exit', 'quit', 'keluar' - Keluar dari program

Tips:
• Gunakan pertanyaan yang spesifik untuk hasil yang lebih baik
• Bot akan mencari informasi dari semua dokumen DPR RI yang tersedia
""")


def main():
    """Main function to run the RAG chatbot system."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        print("Initializing RAG Chatbot...")
        
        # Initialize document processor
        processor = DocumentProcessor()
        
        # Check if we need to process documents
        documents_folder = input("Enter path to documents folder (or press Enter to skip): ").strip()
        if documents_folder and os.path.exists(documents_folder):
            print(f"Processing documents from: {documents_folder}")
            results = processor.process_multiple_documents(documents_folder)
            print(f"Processing complete: {results['success']} success, {results['failed']} failed")
        else:
            print("Skipping document processing. Using existing data if available.")
        
        # Initialize chatbot
        chatbot = RAGChatbot(processor)
        
        # Start chat loop
        chatbot.chat_loop()
        
    except Exception as e:
        logging.error(f"Error in main: {e}")
        print(f"Failed to start chatbot: {e}")


if __name__ == "__main__":
    main()