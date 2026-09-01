from pathlib import Path

from app.core.config import settings


def save_file(
    file_content: bytes,
    filename: str,
) -> Path:
    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = settings.upload_dir / filename

    file_path.write_bytes(file_content)

    return file_path


def delete_file(file_path: Path):
    if file_path.exists():
        file_path.unlink()