from langchain_google_genai._common import GoogleGenerativeAIError

from app.core.exceptions import AIServiceRateLimitException
from app.vectorstore.chroma import get_vector_store
from app.core.config import settings

def retrieve_documents(
    query: str,
    document_id: str,
):
    vector_store = get_vector_store()

    try:
        documents = vector_store.similarity_search(
            query=query,
            k=settings.top_k,
            filter={
                "document_id": document_id,
            },
        )

    except GoogleGenerativeAIError as exc:
        if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
            raise AIServiceRateLimitException() from exc

        raise

    return documents