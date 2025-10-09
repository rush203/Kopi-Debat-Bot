"""Tests for the debate API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.schemas import MessageRole

client = TestClient(app)


class TestHealthCheck:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root(self):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data


class TestDebateEndpoint:
    """Tests for debate endpoint."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_new_conversation(self, mock_generate):
        """Test creating a new conversation."""
        mock_generate.return_value = "I strongly believe the Earth is flat because..."
        
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "I think the Earth is flat"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "conversation_id" in data
        assert data["conversation_id"] is not None
        assert "message" in data
        assert isinstance(data["message"], list)
        
        # Check messages
        messages = data["message"]
        assert len(messages) == 2  # User message + bot response
        assert messages[0]["role"] == "user"
        assert messages[0]["message"] == "I think the Earth is flat"
        assert messages[1]["role"] == "bot"
        assert messages[1]["message"] == "I strongly believe the Earth is flat because..."
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_continue_conversation(self, mock_generate):
        """Test continuing an existing conversation."""
        # First, create a conversation
        mock_generate.return_value = "Initial bot response"
        
        create_response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Climate change is real"
            }
        )
        
        conversation_id = create_response.json()["conversation_id"]
        
        # Continue the conversation
        mock_generate.return_value = "Here's why you're wrong about that..."
        
        continue_response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": conversation_id,
                "message": "But what about the scientific consensus?"
            }
        )
        
        assert continue_response.status_code == 200
        data = continue_response.json()
        
        assert data["conversation_id"] == conversation_id
        messages = data["message"]
        assert len(messages) == 4  # 2 user + 2 bot messages
    
    def test_invalid_conversation_id(self):
        """Test using an invalid conversation ID."""
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": "non-existent-id",
                "message": "Hello"
            }
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_empty_message(self):
        """Test sending an empty message."""
        response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": ""
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_message_history_limit(self, mock_generate):
        """Test that message history is limited to recent messages."""
        mock_generate.return_value = "Bot response"
        
        # Create conversation
        create_response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Message 1"
            }
        )
        
        conversation_id = create_response.json()["conversation_id"]
        
        # Add multiple messages (more than the limit)
        for i in range(2, 8):
            client.post(
                "/api/v1/debate",
                json={
                    "conversation_id": conversation_id,
                    "message": f"Message {i}"
                }
            )
        
        # Get final response
        final_response = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": conversation_id,
                "message": "Final message"
            }
        )
        
        data = final_response.json()
        messages = data["message"]
        
        # Should only return last 5 pairs (10 messages max)
        assert len(messages) <= 10


class TestConversationManager:
    """Tests for conversation management."""
    
    @patch('app.services.debate_bot.debate_bot.generate_response')
    def test_multiple_conversations(self, mock_generate):
        """Test managing multiple separate conversations."""
        mock_generate.return_value = "Response"
        
        # Create first conversation
        conv1 = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Earth is flat"
            }
        )
        conv1_id = conv1.json()["conversation_id"]
        
        # Create second conversation
        conv2 = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": None,
                "message": "Vaccines are safe"
            }
        )
        conv2_id = conv2.json()["conversation_id"]
        
        # Verify they're different
        assert conv1_id != conv2_id
        
        # Continue both conversations
        response1 = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": conv1_id,
                "message": "More about flat earth"
            }
        )
        
        response2 = client.post(
            "/api/v1/debate",
            json={
                "conversation_id": conv2_id,
                "message": "More about vaccines"
            }
        )
        
        # Both should work independently
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["conversation_id"] == conv1_id
        assert response2.json()["conversation_id"] == conv2_id

