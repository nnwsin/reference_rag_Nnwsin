from pydantic import BaseModel


from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1)


class Source(BaseModel):
    filename: str
    page: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]