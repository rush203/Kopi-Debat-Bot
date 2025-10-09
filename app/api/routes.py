"""API route handlers."""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import DebateRequest, DebateResponse, MessageRole
from app.services.conversation import conversation_manager
from app.services.debate_bot import debate_bot
from app.config import settings

router = APIRouter()


@router.post("/debate", response_model=DebateResponse, status_code=status.HTTP_200_OK)
async def debate(request: DebateRequest) -> DebateResponse:
    """
    Main debate endpoint.
    
    Handles both new conversations (conversation_id is null) and
    continuing conversations (conversation_id provided).
    """
    # Case 1: New conversation
    if request.conversation_id is None:
        # Create new conversation
        conversation_id, topic, stance = conversation_manager.create_conversation(
            request.message
        )
        conversation = conversation_manager.get_conversation(conversation_id)
        
        # Generate bot's initial response
        bot_response = debate_bot.generate_response(
            topic=topic,
            stance=stance,
            conversation_history=[],
            current_message=request.message
        )
        
        # Add bot response to conversation
        conversation_manager.add_bot_message(conversation_id, bot_response)
        conversation = conversation_manager.get_conversation(conversation_id)
        
        # Return response with recent messages
        return DebateResponse(
            conversation_id=conversation_id,
            message=conversation.get_recent_messages(settings.max_history_messages)
        )
    
    # Case 2: Continuing conversation
    else:
        conversation = conversation_manager.get_conversation(request.conversation_id)
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found or expired"
            )
        
        # Add user message
        conversation_manager.add_user_message(request.conversation_id, request.message)
        
        # Get conversation history (excluding the just-added message for context)
        history = conversation.get_full_history()[:-1]
        
        # Generate bot response
        bot_response = debate_bot.generate_response(
            topic=conversation.topic,
            stance=conversation.stance,
            conversation_history=history,
            current_message=request.message
        )
        
        # Add bot response
        conversation_manager.add_bot_message(request.conversation_id, bot_response)
        
        # Refresh conversation
        conversation = conversation_manager.get_conversation(request.conversation_id)
        
        # Return response with recent messages
        return DebateResponse(
            conversation_id=request.conversation_id,
            message=conversation.get_recent_messages(settings.max_history_messages)
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


