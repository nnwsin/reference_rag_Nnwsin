from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.services.retrieval_service import retrieve_documents
from app.services.llm_service import get_llm


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
async def chat(request: ChatRequest):
    documents = retrieve_documents(
        query=request.question,
        document_id=request.document_id,
    )
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

    llm = get_llm()

    response = await llm.ainvoke(prompt)

    return {
        "answer": response.content,
    }