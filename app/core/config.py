from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str

    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

    max_upload_size_mb: int = 10

    chroma_dir: Path = Path("data/chroma")
    upload_dir: Path = Path("data/uploads")
    metadata_file: Path = Path("data/documents.json")

    allowed_extensions: set[str] = {
        ".pdf",
        ".docx",
        ".txt",
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()