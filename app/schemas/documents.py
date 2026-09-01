from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: str
    original_filename: str
    stored_filename: str
    content_type: str | None = None
    file_path: str
    chunks_created: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    count: int


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str | None = None
    chunks_created: int
    message: str


class DocumentDeleteResponse(BaseModel):
    document_id: str
    message: str