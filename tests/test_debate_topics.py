"""Enhanced tests for various debate topics and scenarios."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestFlatEarthDebate:
    """Tests for flat earth debate topic."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_flat_earth_pro_position(self, mock_generate):
        """Test bot defending flat earth theory."""
        mock_generate.return_value = (
            "Absolutely! The evidence for a flat Earth is compelling. Consider that "
            "water always finds its level - we've never observed curved water, yet if "
            "Earth were a spinning ball, oceans would curve dramatically."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "I believe the Earth is flat and here's why..."
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "flat" in data["message"][-1]["message"].lower() or "earth" in data["message"][-1]["message"].lower()
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_flat_earth_multi_turn(self, mock_generate):
        """Test multi-turn flat earth debate."""
        # Start conversation
        mock_generate.return_value = "Flat earth evidence..."
        response = client.post(
            "/api/v1/debate",
            json={"conversation_id": None, "message": "Earth is flat"}
        )
        conv_id = response.json()["conversation_id"]
        
        # Turn 2
        mock_generate.return_value = "Satellite images are CGI composites..."
        response = client.post(
            "/api/v1/debate",
            json={"conversation_id": conv_id, "message": "What about satellite images?"}
        )
        assert response.status_code == 200
        
        # Turn 3
        mock_generate.return_value = "Horizon always at eye level..."
        response = client.post(
            "/api/v1/debate",
            json={"conversation_id": conv_id, "message": "How do you explain ships disappearing?"}
        )
        assert response.status_code == 200
        assert len(response.json()["message"]) == 6  # 3 pairs


class TestClimateChangeDebate:
    """Tests for climate change debate topic."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_climate_skeptic_position(self, mock_generate):
        """Test bot taking climate skeptic position."""
        mock_generate.return_value = (
            "While many claim climate change is a crisis, we must examine the data "
            "critically. Historical records show Earth has gone through natural warming "
            "and cooling cycles long before human industrial activity."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Climate change is just natural Earth cycles, not human-caused"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert len(data["message"]) == 2
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_climate_pro_action_position(self, mock_generate):
        """Test bot defending climate action."""
        mock_generate.return_value = (
            "The scientific consensus is overwhelming - 97% of climate scientists agree "
            "that climate change is real and human-caused. We're seeing unprecedented "
            "warming rates, melting ice caps, and extreme weather events."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Climate change is the biggest threat facing humanity"
            }
        )
        
        assert response.status_code == 200


class TestVaccinationDebate:
    """Tests for vaccination debate topic."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_pro_vaccine_position(self, mock_generate):
        """Test bot defending vaccines."""
        mock_generate.return_value = (
            "Vaccines are one of the greatest public health achievements in history. "
            "They've eradicated smallpox, nearly eliminated polio, and prevent millions "
            "of deaths annually. The benefits far outweigh the minimal risks."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Vaccines are safe and effective"
            }
        )
        
        assert response.status_code == 200
        assert response.json()["message"][1]["role"] == "bot"
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_vaccine_skeptic_position(self, mock_generate):
        """Test bot taking anti-vaccine stance."""
        mock_generate.return_value = (
            "While mainstream medicine promotes vaccines, we must question the safety "
            "studies funded by pharmaceutical companies with profit motives."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "I'm concerned about vaccine side effects"
            }
        )
        
        assert response.status_code == 200


class TestEvolutionDebate:
    """Tests for evolution debate topic."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_evolution_debate(self, mock_generate):
        """Test evolution vs creationism debate."""
        mock_generate.return_value = (
            "Evolution is supported by overwhelming evidence from multiple scientific "
            "disciplines - fossil records, DNA analysis, observed speciation, and "
            "biogeography all confirm the theory of evolution by natural selection."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Evolution is just a theory with no proof"
            }
        )
        
        assert response.status_code == 200


class TestMoonLandingDebate:
    """Tests for moon landing conspiracy debate."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_moon_landing_skeptic(self, mock_generate):
        """Test moon landing conspiracy position."""
        mock_generate.return_value = (
            "There are numerous inconsistencies in the moon landing footage. "
            "The flag appears to wave in a vacuum, shadows go different directions, "
            "and no stars are visible in the photographs."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "The moon landing was faked in a Hollywood studio"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["message"]) == 2


class TestPoliticalDebates:
    """Tests for political debate topics."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_economic_policy_debate(self, mock_generate):
        """Test economic policy debate."""
        mock_generate.return_value = (
            "Free market capitalism has lifted more people out of poverty than any "
            "other economic system in history. Competition drives innovation and "
            "efficiency, creating prosperity for all."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Universal basic income is necessary in the age of automation"
            }
        )
        
        assert response.status_code == 200
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_healthcare_debate(self, mock_generate):
        """Test healthcare policy debate."""
        mock_generate.return_value = (
            "Universal healthcare ensures everyone has access to medical care regardless "
            "of their ability to pay. It's a human right, not a privilege for the wealthy."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Healthcare should be a universal right"
            }
        )
        
        assert response.status_code == 200


class TestTechnologyDebates:
    """Tests for technology-related debates."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_ai_safety_debate(self, mock_generate):
        """Test AI safety debate."""
        mock_generate.return_value = (
            "AI poses existential risks to humanity. As AI systems become more capable, "
            "we risk creating superintelligent systems we cannot control or align with "
            "human values."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "AI will be humanity's greatest invention"
            }
        )
        
        assert response.status_code == 200
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_privacy_debate(self, mock_generate):
        """Test digital privacy debate."""
        mock_generate.return_value = (
            "Privacy is a fundamental human right in the digital age. Mass surveillance "
            "and data collection by corporations and governments threaten our freedom "
            "and autonomy."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "If you have nothing to hide, you have nothing to fear"
            }
        )
        
        assert response.status_code == 200


class TestSocialDebates:
    """Tests for social issue debates."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_education_debate(self, mock_generate):
        """Test education policy debate."""
        mock_generate.return_value = (
            "Free college education is an investment in our future. An educated populace "
            "drives innovation, economic growth, and social progress. Countries with "
            "free higher education have higher standards of living."
        )
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "College should be free for everyone"
            }
        )
        
        assert response.status_code == 200


class TestLongDebateConversation:
    """Test extended debate conversations."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_ten_turn_conversation(self, mock_generate):
        """Test a debate lasting 10+ exchanges."""
        mock_generate.return_value = "Compelling argument..."
        
        # Start conversation
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Cryptocurrency will replace traditional money"
            }
        )
        conv_id = response.json()["conversation_id"]
        
        # Continue for 9 more turns
        arguments = [
            "What about government regulation?",
            "But crypto is volatile and risky",
            "How do you address energy consumption?",
            "What about transaction speeds?",
            "Governments will ban it",
            "It's used for illegal activities",
            "What about scalability issues?",
            "Traditional banks are more reliable",
            "Crypto has no intrinsic value"
        ]
        
        for i, argument in enumerate(arguments, 1):
            mock_generate.return_value = f"Response to argument {i}"
            response = client.post(
                "/api/v1/debate",
                json={"conversation_id": conv_id, "message": argument}
            )
            assert response.status_code == 200
        
        # Final response should have limited history (last 5 pairs = 10 messages)
        final_data = response.json()
        assert len(final_data["message"]) <= 10
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_debate_coherence_over_turns(self, mock_generate):
        """Test that debate remains coherent over multiple turns."""
        # Set initial response for first message
        mock_generate.return_value = "Artificial meat can feed the world sustainably..."
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Lab-grown meat is the future of food"
            }
        )
        conv_id = response.json()["conversation_id"]
        
        responses = [
            "Traditional livestock farming causes massive environmental damage...",
            "Lab-grown meat eliminates animal suffering...",
            "The technology will become cost-effective at scale...",
            "Consumer acceptance is growing rapidly..."
        ]
        
        for i, bot_response in enumerate(responses):
            mock_generate.return_value = bot_response
            response = client.post(
                "/api/v1/debate",
                json={
                    "conversation_id": conv_id,
                    "message": f"Counter argument {i+1}"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["conversation_id"] == conv_id


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_very_long_user_message(self, mock_generate):
        """Test handling of very long user messages."""
        mock_generate.return_value = "I understand your detailed point..."
        
        long_message = " ".join(["This is a very detailed argument."] * 100)
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": long_message
            }
        )
        
        assert response.status_code == 200
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_special_characters_in_message(self, mock_generate):
        """Test handling of special characters."""
        mock_generate.return_value = "Interesting point about symbols..."
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "What about $money$ & <tags> and 'quotes' and \"more quotes\"?"
            }
        )
        
        assert response.status_code == 200
        
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_unicode_in_message(self, mock_generate):
        """Test handling of unicode characters."""
        mock_generate.return_value = "I understand your point..."
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "¿Cómo está? 你好 مرحبا 🌍 Debate about émojis!"
            }
        )
        
        assert response.status_code == 200


class TestPerformance:
    """Test performance characteristics."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_concurrent_conversations(self, mock_generate):
        """Test handling multiple concurrent conversations."""
        mock_generate.return_value = "Response"
        
        # Create 10 different conversations
        conversation_ids = []
        for i in range(10):
            response = client.post(
                "/api/v1/debate",
                json={
                    "conversation_id": None,
                    "message": f"Debate topic {i}"
                }
            )
            assert response.status_code == 200
            conversation_ids.append(response.json()["conversation_id"])
        
        # Verify all conversations are unique
        assert len(set(conversation_ids)) == 10
        
        # Continue all conversations
        for conv_id in conversation_ids:
            response = client.post(
                "/api/v1/debate",
                json={
                    "conversation_id": conv_id,
                    "message": "Follow up question"
                }
            )
            assert response.status_code == 200

