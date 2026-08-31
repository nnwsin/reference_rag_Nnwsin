import json
from pathlib import Path


METADATA_FILE = Path("data/documents.json")


def save_document_metadata(document: dict):
    documents = []

    if METADATA_FILE.exists():
        documents = json.loads(
            METADATA_FILE.read_text(encoding="utf-8")
        )

    documents.append(document)

    METADATA_FILE.write_text(
        json.dumps(documents, indent=4),
        encoding="utf-8",
    )


def get_all_documents():
    if not METADATA_FILE.exists():
        return []

    return json.loads(
        METADATA_FILE.read_text(encoding="utf-8")
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

    METADATA_FILE.write_text(
        json.dumps(updated_documents, indent=4),
        encoding="utf-8",
    )

    return True