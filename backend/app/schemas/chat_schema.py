from pydantic import BaseModel
from typing import Any, Optional, Dict


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    intent: str
    data: Optional[Any] = None
    chart: Optional[Dict[str, Any]] = None
