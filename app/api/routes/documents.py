from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.repositories.document_repository import (
    delete_document_metadata,
    get_all_documents,
    get_document,
    save_document_metadata,
)

from app.vectorstore.chroma import delete_documents
from app.services.ingestion_service import ingest_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    document_id = str(uuid4())

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    file_path = UPLOAD_DIR / f"{document_id}{extension}"

    try:
        file_content = await file.read()
        file_path.write_bytes(file_content)

        chunks = ingest_document(
            file_path=file_path,
            document_id=document_id,
            original_filename=file.filename,
        )

        save_document_metadata(
                {
                    "document_id": document_id,
                    "original_filename": file.filename,
                    "stored_filename": file_path.name,
                    "content_type": file.content_type,
                    "file_path": str(file_path),
                    "chunks_created": len(chunks),
                }
            )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the uploaded document.",
        ) from exc

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "chunks_created": len(chunks),
        "message": "Document uploaded and indexed successfully",
    }


@router.get("")
async def get_documents():
    documents = get_all_documents()

    return {
        "documents": documents,
        "count": len(documents),
    }


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    file_path = Path(document["file_path"])

    try:
        delete_documents(document_id)

        if file_path.exists():
            file_path.unlink()

        delete_document_metadata(document_id)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete the document.",
        ) from exc

    return {
        "document_id": document_id,
        "message": "Document deleted successfully",
    }