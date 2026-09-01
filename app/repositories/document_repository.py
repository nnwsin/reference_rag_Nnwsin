import json
from app.core.config import settings


def save_document_metadata(document: dict):
    documents = []

    if settings.metadata_file.exists():
        documents = json.loads(
            settings.metadata_file.read_text(encoding="utf-8")
        )

    documents.append(document)

    settings.metadata_file.parent.mkdir(parents=True, exist_ok=True)
    settings.metadata_file.write_text(
        json.dumps(documents, indent=4),
        encoding="utf-8",
    )


def get_all_documents():
    if not settings.metadata_file.exists():
        return []

    return json.loads(
        settings.metadata_file.read_text(encoding="utf-8")
    )


def get_document(document_id: str):
    documents = get_all_documents()

    return next(
        (
            document
            for document in documents
            if document["document_id"] == document_id
        ),
        None,
    )


def delete_document_metadata(document_id: str):
    documents = get_all_documents()

    updated_documents = [
        document
        for document in documents
        if document["document_id"] != document_id
    ]

    if len(updated_documents) == len(documents):
        return False

    settings.metadata_file.parent.mkdir(parents=True, exist_ok=True)
    settings.metadata_file.write_text(
        json.dumps(updated_documents, indent=4),
        encoding="utf-8",
    )

    return True
