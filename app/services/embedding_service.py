from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings


def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.gemini_api_key,
    )
