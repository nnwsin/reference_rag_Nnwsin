from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.documents import router as documents_router


load_dotenv()


app = FastAPI(
    title="Document RAG API",
    description="RAG-based API for asking questions about uploaded documents",
    version="1.0.0",
)


app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Document RAG API is running"}