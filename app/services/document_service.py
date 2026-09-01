from app.core.exceptions import FileTooLargeException
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.repositories.document_repository import save_document_metadata
from app.services.ingestion_service import ingest_document
from app.storage.file_storage import save_file

async def save_uploaded_document(file: UploadFile) -> tuple[str, Path]:
    document_id = str(uuid4())

    extension = Path(file.filename).suffix.lower()

    max_size = settings.max_upload_size_mb * 1024 * 1024

    file_content = await file.read(max_size + 1)

    if len(file_content) > max_size:
        raise FileTooLargeException()

    file_path = save_file(
        file_content=file_content,
        filename=f"{document_id}{extension}",
    )

    return document_id, file_path

def process_document(
    file: UploadFile,
    document_id: str,
    file_path: Path,
):
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

    return chunks