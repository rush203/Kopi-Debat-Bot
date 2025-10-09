"""Pydantic schemas for request/response validation."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role enum."""
    USER = "user"
    BOT = "bot"


class Message(BaseModel):
    """Individual message in conversation history."""
    role: MessageRole
    message: str


class DebateRequest(BaseModel):
    """Request model for debate endpoint."""
    conversation_id: Optional[str] = Field(
        None,
        description="Conversation ID. Null for new conversations."
    )
    message: str = Field(
        ...,
        description="User's message",
        min_length=1
    )


class DebateResponse(BaseModel):
    """Response model for debate endpoint."""
    conversation_id: str = Field(
        ...,
        description="Unique conversation identifier"
    )
    message: List[Message] = Field(
        ...,
        description="Last 5 messages in the conversation (most recent last)",
        max_length=10  # 5 user + 5 bot messages
    )


