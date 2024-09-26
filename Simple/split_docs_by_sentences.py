import nltk
from nltk.tokenize import sent_tokenize
from langchain.schema.document import Document

def split_documents_by_sentences(documents: list[Document], sentences_per_chunk: int = 5):
    chunks = []
    nltk.download('punkt_tab')
    for document in documents:
        text = document.page_content
        sentences = sent_tokenize(text)  # Tokeniza el texto en oraciones.
        
        # Agrupar oraciones en chunks de tamaño fijo.
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            chunk_text = " ".join(chunk_sentences)
            
            # Crear un nuevo documento para cada chunk.
            chunk_doc = Document(
                page_content=chunk_text,
                metadata=document.metadata.copy()  # Copia los metadatos del documento original.
            )
            chunks.append(chunk_doc)
    
    return chunks
