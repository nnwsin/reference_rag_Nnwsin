from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.core.exceptions import (
    DocumentNotFoundException,
    EmptyFileException,
    InvalidFileTypeException,
)
from app.repositories.document_repository import (
    delete_document_metadata,
    get_all_documents,
    get_document,
)
from app.schemas.documents import (
    DocumentDeleteResponse,
    DocumentListResponse,
    DocumentUploadResponse,
)
from app.services.document_service import (
    process_document,
    save_uploaded_document,
)
from app.storage.file_storage import delete_file
from app.vectorstore.chroma import delete_documents


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


settings.upload_dir.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise EmptyFileException()

    extension = Path(file.filename).suffix.lower()

    if extension not in settings.allowed_extensions:
        raise InvalidFileTypeException()

    document_id, file_path = await save_uploaded_document(file)

    chunks = process_document(
        file=file,
        document_id=document_id,
        file_path=file_path,
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "chunks_created": len(chunks),
        "message": "Document uploaded and indexed successfully",
    }


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def get_documents():
    documents = get_all_documents()

    return {
        "documents": documents,
        "count": len(documents),
    }


@router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse,
)
async def delete_document(
    document_id: str,
):
    document = get_document(document_id)

    if document is None:
        raise DocumentNotFoundException()

    file_path = Path(document["file_path"])

    delete_documents(document_id)

    delete_file(file_path)

    delete_document_metadata(document_id)

    return {
        "document_id": document_id,
        "message": "Document deleted successfully",
    }