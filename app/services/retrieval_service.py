from app.vectorstore.chroma import get_vector_store


def retrieve_documents(
    query: str,
    document_id: str,
    k: int = 4,
):
    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query=query,
        k=k,
        filter={
            "document_id": document_id,
        },
    )

    return documents