"""Conversation management service."""

import uuid
from datetime import datetime, timedelta, UTC
from typing import Dict, List, Optional, Tuple
from app.models.schemas import Message, MessageRole
from app.config import settings


class Conversation:
    """Represents a single debate conversation."""
    
    def __init__(self, conversation_id: str, topic: str, stance: str):
        self.conversation_id = conversation_id
        self.topic = topic
        self.stance = stance
        self.messages: List[Message] = []
        self.created_at = datetime.now(UTC)
        self.last_updated = datetime.now(UTC)
    
    def add_message(self, role: MessageRole, message: str) -> None:
        """Add a message to the conversation."""
        self.messages.append(Message(role=role, message=message))
        self.last_updated = datetime.now(UTC)
    
    def get_recent_messages(self, count: int = 5) -> List[Message]:
        """Get the most recent messages (up to count pairs)."""
        # Return last 'count' messages from each side (up to 2*count total)
        return self.messages[-count * 2:] if len(self.messages) > count * 2 else self.messages
    
    def get_full_history(self) -> List[Message]:
        """Get all messages in the conversation."""
        return self.messages.copy()


class ConversationManager:
    """Manages all debate conversations."""
    
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
    
    def create_conversation(self, initial_message: str) -> Tuple[str, str, str]:
        """
        Create a new conversation from the initial message.
        
        Args:
            initial_message: The first user message defining topic and stance
            
        Returns:
            Tuple of (conversation_id, topic, stance)
        """
        conversation_id = str(uuid.uuid4())
        
        # Parse the initial message to extract topic and stance
        # The bot will take a position based on the user's message
        topic, stance = self._parse_initial_message(initial_message)
        
        conversation = Conversation(conversation_id, topic, stance)
        conversation.add_message(MessageRole.USER, initial_message)
        
        self._conversations[conversation_id] = conversation
        
        return conversation_id, topic, stance
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        # Clean up old conversations
        self._cleanup_old_conversations()
        return self._conversations.get(conversation_id)
    
    def add_user_message(self, conversation_id: str, message: str) -> bool:
        """
        Add a user message to an existing conversation.
        
        Returns:
            True if successful, False if conversation not found
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        
        conversation.add_message(MessageRole.USER, message)
        return True
    
    def add_bot_message(self, conversation_id: str, message: str) -> bool:
        """
        Add a bot message to an existing conversation.
        
        Returns:
            True if successful, False if conversation not found
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        
        conversation.add_message(MessageRole.BOT, message)
        return True
    
    def _parse_initial_message(self, message: str) -> Tuple[str, str]:
        """
        Parse the initial message to determine topic and bot's stance.
        
        This is a simple parser. In production, you might use NLP.
        The bot will take a contrarian or defined position.
        """
        # For now, we'll extract the topic from the message and determine stance
        # The stance will be determined by the DebateBot based on context
        message_lower = message.lower()
        
        # Common debate topics and stances
        if "flat" in message_lower and "earth" in message_lower:
            topic = "Shape of the Earth"
            stance = "pro-flat-earth" if "is flat" in message_lower or "flat earth" in message_lower else "against-flat-earth"
        elif "climate" in message_lower:
            topic = "Climate Change"
            stance = "pro-climate-action" if "real" in message_lower or "happening" in message_lower else "climate-skeptic"
        elif "vaccination" in message_lower or "vaccine" in message_lower:
            topic = "Vaccination"
            stance = "pro-vaccine" if "good" in message_lower or "safe" in message_lower else "anti-vaccine"
        else:
            # Generic topic extraction
            topic = "Debate Topic"
            stance = "contrarian"
        
        return topic, stance
    
    def _cleanup_old_conversations(self) -> None:
        """Remove conversations older than the timeout period."""
        cutoff_time = datetime.now(UTC) - timedelta(
            seconds=settings.conversation_timeout_seconds
        )
        
        expired_ids = [
            conv_id for conv_id, conv in self._conversations.items()
            if conv.last_updated < cutoff_time
        ]
        
        for conv_id in expired_ids:
            del self._conversations[conv_id]


# Global conversation manager instance
conversation_manager = ConversationManager()

