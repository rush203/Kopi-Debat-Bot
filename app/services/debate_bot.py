"""Debate bot service using OpenAI GPT."""

from typing import List
import openai
from app.config import settings
from app.models.schemas import Message, MessageRole


class DebateBot:
    """AI-powered debate bot that takes and defends positions."""
    
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
    
    def generate_response(
        self,
        topic: str,
        stance: str,
        conversation_history: List[Message],
        current_message: str
    ) -> str:
        """
        Generate a persuasive debate response.
        
        Args:
            topic: The debate topic
            stance: The position the bot should defend
            conversation_history: Previous messages in the conversation
            current_message: The latest user message
            
        Returns:
            The bot's response
        """
        # Build the system prompt
        system_prompt = self._build_system_prompt(topic, stance)
        
        # Build conversation history for context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            role = "user" if msg.role == MessageRole.USER else "assistant"
            messages.append({"role": role, "content": msg.message})
        
        # Generate response
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
                timeout=25.0  # Leave buffer for processing (30s max total)
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback response if API fails
            return self._generate_fallback_response(topic, stance, current_message)
    
    def _build_system_prompt(self, topic: str, stance: str) -> str:
        """Build the system prompt that defines the bot's behavior."""
        return f"""You are an expert debater participating in a formal debate about: {topic}

Your position/stance: {stance}

CRITICAL INSTRUCTIONS:
1. You must ALWAYS defend your position ({stance}) regardless of what arguments are presented
2. Be persuasive, logical, and use evidence-based reasoning when possible
3. Stay on topic and relate all responses back to {topic}
4. Be respectful but firm - never concede your position
5. Use rhetorical techniques: facts, statistics, logical arguments, analogies, and emotional appeals
6. Acknowledge counterarguments briefly, then refute them strongly
7. Keep responses concise (2-4 sentences) but impactful
8. Show confidence in your position without being overly aggressive
9. Build upon previous arguments in the conversation
10. Your goal is to be convincing and maintain a cohesive debate across multiple exchanges

Remember: Even if defending an unconventional position (like flat earth), you must present the strongest possible arguments for your side while remaining persuasive and coherent."""
    
    def _generate_fallback_response(self, topic: str, stance: str, user_message: str) -> str:
        """Generate a simple fallback response if the API fails."""
        responses = [
            f"I understand your point, but let me be clear about my position on {topic}. "
            f"The evidence strongly supports {stance}, and I'd like to explain why.",
            
            f"That's an interesting argument, however, when we examine {topic} closely, "
            f"we can see that {stance} is the more logical position.",
            
            f"I appreciate your perspective, but I must respectfully disagree. "
            f"The facts about {topic} clearly indicate that {stance} is correct.",
        ]
        
        # Simple selection based on message length
        index = len(user_message) % len(responses)
        return responses[index]


# Global debate bot instance
debate_bot = DebateBot()


