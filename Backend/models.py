from pydantic import BaseModel, Field
from typing import Union

# Request body for user message
class UserMessage(BaseModel):
    message: str

class MessageResponse(BaseModel):
    status: int
    message: str