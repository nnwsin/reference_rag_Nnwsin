from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.api.routes.chat import router as chat_router
from app.api.routes.documents import router as documents_router


app = FastAPI(
    title="Document RAG API",
    description="RAG-based API for asking questions about uploaded documents",
    version="1.0.0",
)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred.",
        },
    )


app.include_router(documents_router)
app.include_router(chat_router)
