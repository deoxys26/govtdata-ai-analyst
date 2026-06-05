from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import answer_question


router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_question(request: ChatRequest):
    return answer_question(request.question)
