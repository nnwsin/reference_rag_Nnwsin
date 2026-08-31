from pathlib import Path

from app.loaders.document_loader import load_document
from app.loaders.text_splitter import split_documents
from app.vectorstore.chroma import get_vector_store


def ingest_document(
        file_path: Path,
        document_id: str,
        original_filename: str,
    ):
    documents = load_document(file_path)

    chunks = split_documents(documents)

    for chunk in chunks:
        chunk.metadata["document_id"] = document_id
        chunk.metadata["filename"] = original_filename

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    return chunks