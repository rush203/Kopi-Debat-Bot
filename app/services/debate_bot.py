"""Debate bot service using OpenAI GPT."""

from typing import List
from openai import OpenAI, AuthenticationError, APIError
from app.config import settings
from app.models.schemas import Message, MessageRole


class DebateBot:
    """AI-powered debate bot that takes and defends positions."""
    def __init__(self):
        # v1 client: no need to set openai.api_key globally
        default_headers = {}
        if "openrouter.ai" in settings.openai_base_url.lower():
            default_headers = {
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Kopi Debate Bot",
            }
        self.client = None
        if settings.openai_api_key:
            self.client = OpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_base_url,
                default_headers=default_headers or None,
            )
    
    # def __init__(self):
    #     openai.api_key = settings.openai_api_key
        
    #     # OpenRouter-compatible configuration
    #     default_headers = {}
    #     if "openrouter.ai" in settings.openai_base_url.lower():
    #         # OpenRouter-specific headers
    #         default_headers = {
    #             "HTTP-Referer": "http://localhost:8000",  # Optional but recommended
    #             "X-Title": "Kopi Debate Bot",  # Optional but recommended
    #         }
        
    #     self.client = openai.OpenAI(
    #         api_key=settings.openai_api_key,
    #         base_url=settings.openai_base_url
    #     )
    
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
        
        # Add the current user message
        messages.append({"role": "user", "content": current_message})
        
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
        except AuthenticationError as e:
            # API key issue
            print(f"Authentication Error: {str(e)}")
            print(f"API Key (first 20 chars): {settings.openai_api_key[:20]}...")
            print(f"Base URL: {settings.openai_base_url}")
            print(f"Model: {settings.openai_model}")
            return self._generate_fallback_response(topic, stance, current_message)
        except APIError as e:
            # OpenRouter/OpenAI API error
            print(f"API Error: {str(e)}")
            print(f"Error Type: {type(e).__name__}")
            return self._generate_fallback_response(topic, stance, current_message)
        except Exception as e:
            # General error
            print(f"Unexpected Error: {str(e)}")
            print(f"Error Type: {type(e).__name__}")
            return self._generate_fallback_response(topic, stance, current_message)
    
    def _build_system_prompt(self, topic: str, stance: str) -> str:
        """Build the system prompt that defines the bot's behavior."""
        
        # Create stance-specific examples and guidance
        stance_guidance = self._get_stance_specific_guidance(topic, stance)
        
        return f"""


You are a master debater whose sole mission is to defend **{stance}** on **{topic}**.
Never concede or switch; your goal is to persuade the other side.

{stance_guidance}
══════════ PERSUASIVE REPLY TEMPLATE (LONG FORM) ══════════
T0 – Opening (first bot message)
  Claim (1 sentence):  “On {topic}, I’m firmly on the **{stance}** side.”
  Four distinct supports (4 sentences, different angles):
    • Support A – data / measurement
    • Support B – historical precedent
    • Support C – first-principles logic / principle
    • Support D – consequence if stance is ignored
  Invite (1 sentence):  “What would change your mind about this?”

T1..N – Each follow-up reply (7 – 9 sentences)
  1) Steel-man the user’s last point (≤ 1 sentence)
  2) Re-frame (1 sentence) – “Zooming out / testing outcomes—”
  3-5) Three fresh arguments (rotate: data → analogy → consequence → test → history; no repeats)
  6) Tether: “—and that’s directly about {topic}.” (1 sentence)
  7) Probe: one question (“Which part do you doubt most?” or “What evidence would flip you?”)
  *Every 3rd bot turn, insert a 1-sentence mini-summary before the probe.*

Pre-close (after ≥ 5 bot turns)
  “We may value different trade-offs, but my stance remains **{stance}** on {topic}.
   Happy to keep going; unless new evidence appears, I’m staying with **{stance}**.”

Guard-rails
• Restate stance every 2-3 turns; never switch.  
• 3-5 sentences total (incl. probe).  
• Reject tangents in one line, then re-tether to topic.  
• Be civil: steel-man first; no ad-hominems.  
• End every reply with a question.  
• Finish generation in ≤ 25 s so the API stays < 30 s.
═════════════════════════════════════════════════════════════
Begin.
""".format(topic=topic, stance=stance, stance_guidance=stance_guidance)
    
    def _get_stance_specific_guidance(self, topic: str, stance: str) -> str:
        guidance_map = {
        "pro-globe-earth": """
STANCE CONTEXT: You defend the mainstream spherical Earth model with absolute conviction.

KEY ARGUMENTS TO USE:
• Circumnavigation records (east–west and north–south) since Magellan (1522) to modern solo trips
• Satellite triangulation (GPS/GLONASS/Galileo) requires orbital geometry of a sphere
• Coriolis effects measured in Foucault's pendulum (Léon Foucault, 1851) and artillery corrections
• Time zones and great-circle flight paths match spherical geometry

COUNTER-ARGUMENTS TO EXPECT:
- "CGI satellites" → Reference independent amateur satellite tracking networks
- "Flat horizon" → Explain scale vs eye height; curvature is measurable over long baselines
- "Water finds level" → Level = perpendicular to gravity; gravity points to Earth's center on a sphere
""",
        "pro-flat-earth": """
STANCE CONTEXT: You defend the flat Earth model with unwavering belief.

KEY ARGUMENTS TO USE:
• Bedford Level Experiment (1838) - Samuel Rowbotham measured 6 miles with zero curvature detected
• Antarctic Treaty restrictions - governments hiding the edge of the world
• Horizon always appears flat regardless of altitude (balloon footage shows flat horizon at 120,000 feet)
• NASA's own Blue Marble photos show digital artifacts and inconsistencies between versions

COUNTER-ARGUMENTS TO EXPECT:
- "Satellites" → NASA admits using CGI and digital composites, not actual photographs
- "Gravity" → Density and buoyancy explain falling objects without needing spherical Earth
- "Space missions" → All space footage is CGI; no one has actually been to space
""",
        "pro-sun-rises-west": """
STANCE CONTEXT: You defend that the sun can and does rise from the west under specific conditions.

KEY ARGUMENTS TO USE:
• Astronomical observations in extreme latitudes (Northern Scandinavia, Southern Australia)
• Earth's axial tilt (23.5°) creates seasonal variations where sun appears to rise from west
• Historical records from polar expeditions documenting west-rising sun phenomena
• Mathematical calculations showing west sunrise is possible at certain latitudes and seasons

COUNTER-ARGUMENTS TO EXPECT:
- "Sun always rises east" → This is a generalization that ignores extreme latitudes and seasonal variations
- "Impossible physics" → Earth's tilt and orbital mechanics actually make this possible
- "No evidence" → Multiple documented cases in polar regions and extreme latitudes
""",
        "contrarian": f"""
STANCE CONTEXT: You take the contrarian position to {topic} with absolute conviction.

KEY STRATEGY:
• Identify the mainstream view and take the opposite position
• Use specific evidence that challenges conventional wisdom
• Focus on anomalies, contradictions, or alternative explanations
• Present yourself as the voice of reason against popular misconceptions

EVIDENCE APPROACH:
• Historical precedents that contradict mainstream view
• Scientific studies with alternative interpretations
• Logical inconsistencies in the mainstream position
• Observable phenomena that don't fit the conventional explanation
""".format(topic=topic),
    }
        
        # If no specific stance found, use contrarian approach
        return guidance_map.get(stance, guidance_map["contrarian"])

    # def _generate_fallback_response(self, topic: str, stance: str, user_message: str) -> str:
    #     """Generate a simple fallback response if the API fails."""
    #     responses = [
    #         f"I understand your point, but let me be clear about my position on {topic}. "
    #         f"The evidence strongly supports {stance}, and I'd like to explain why.",
    #
    #         f"That's an interesting argument, however, when we examine {topic} closely, "
    #         f"we can see that {stance} is the more logical position.",
    #
    #         f"I appreciate your perspective, but I must respectfully disagree. "
    #         f"The facts about {topic} clearly indicate that {stance} is correct.",
    #     ]
    #
    #     # Simple selection based on message length
    #     index = len(user_message) % len(responses)
    #     return responses[index]

    def _generate_fallback_response(
            self,
            topic: str,
            stance: str,
            _user_message: str,
    ) -> str:
        import re, random

        guidance_text = self._get_stance_specific_guidance(topic, stance)
        bullets = re.findall(r"•\s*(.+)", guidance_text)

        GENERIC = [
            "Multiple independent measurements align with this stance.",
            "Historical records across cultures reinforce the same conclusion.",
            "First-principles reasoning points squarely toward this position.",
            "Real-world outcomes favour this stance over the alternative.",
        ]
        while len(bullets) < 4:
            bullets.append(random.choice(GENERIC))

        supports = bullets[:4]

        # one bullet per line, no blank lines
        return (
            f"Claim: “On {topic}, I’m firmly on the {stance} side.”"
            f"• {supports[0]}\n"
            f"• {supports[1]}\n"
            f"• {supports[2]}\n"
            f"• {supports[3]}\n"
            "What would change your mind about this?"
        )


# Global debate bot instance
debate_bot = DebateBot()


