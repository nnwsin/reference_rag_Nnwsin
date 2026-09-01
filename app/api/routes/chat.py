from fastapi import APIRouter

from app.core.exceptions import DocumentNotFoundException
from app.repositories.document_repository import get_document
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import get_llm
from app.services.retrieval_service import retrieve_documents

from app.services.source_service import build_sources



router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Validate that the requested document exists
    document = get_document(request.document_id)

    if document is None:
        raise DocumentNotFoundException()

    # Retrieve relevant chunks from the requested document
    documents = retrieve_documents(
        query=request.question,
        document_id=request.document_id,
    )

    # No relevant information found
    if not documents:
        return {
            "answer": "I could not find relevant information in the provided document.",
            "sources": [],
        }

    # Build context from retrieved chunks
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{request.question}
"""

    # Generate answer using the LLM
    llm = get_llm()

    response = await llm.ainvoke(prompt)

    # Normalize Gemini's response into a plain string
    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        )

        if isinstance(response.content, str):
            answer = response.content
        else:
            answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        )

        sources = build_sources(documents)

        return {
            "answer": answer,
            "sources": sources,
        }