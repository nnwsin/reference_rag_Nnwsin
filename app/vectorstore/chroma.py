from pathlib import Path

from langchain_chroma import Chroma

from app.services.embedding_service import get_embedding_model


CHROMA_DIR = Path("data/chroma")


def get_vector_store():
    embedding_model = get_embedding_model()

    return Chroma(
        collection_name="documents",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )


def delete_documents(document_id: str):
    vector_store = get_vector_store()

    vector_store.delete(
        where={"document_id": document_id}
    )