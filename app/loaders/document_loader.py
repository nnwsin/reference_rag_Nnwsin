from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)


def load_document(file_path: Path):
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(file_path))

    elif extension == ".docx":
        loader = UnstructuredWordDocumentLoader(str(file_path))

    elif extension == ".txt":
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return loader.load()