# Kopi Debate Bot 🗣️

An AI-powered debate chatbot API that takes positions on topics and defends them persuasively, even if the position is unconventional (like defending flat earth theory). Built with FastAPI, OpenRouter AI, and Docker. Hosted on Railway.

## 🌟 Features

- **Persuasive Debate**: Uses OpenRouter AI models to generate convincing, coherent arguments
- **Position Defense**: Maintains stance throughout conversation regardless of counterarguments
- **Conversation Management**: Tracks multiple simultaneous debates with conversation history
- **Professional Architecture**: Clean separation of concerns, type safety, comprehensive tests
- **Production Ready**: Dockerized, health checks, proper error handling, 30s response time compliance
- **RESTful API**: Well-documented API with OpenAPI/Swagger documentation

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (required): [Installation Guide](https://docs.docker.com/get-docker/)
- **Docker Compose** (required): Usually included with Docker Desktop

The `make install` command will check for these dependencies and provide installation instructions if missing.

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd Kopi

# Install dependencies and setup
make install
```

### 2. Configure Environment

Edit the `.env` file and add your OpenRouter API key:

```bash
# .env
OPENAI_API_KEY=sk-or-your-actual-openrouter-api-key-here
```

### 3. Run the Service

```bash
make run
```

The API will be available at:
- **API Endpoint**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📖 API Documentation

### Endpoint: `POST /api/v1/debate`

The main debate endpoint for starting and continuing conversations.

#### Starting a New Conversation

**Request:**
```json
{
    "conversation_id": null,
    "message": "I believe the Earth is flat and I can prove it"
}
```

**Response:**
```json
{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": [
        {
            "role": "user",
            "message": "I believe the Earth is flat and I can prove it"
        },
        {
            "role": "bot",
            "message": "Absolutely! The evidence for a flat Earth is compelling. Consider that water always finds its level - we've never observed curved water, yet if Earth were a spinning ball, oceans would curve dramatically. Additionally, pilots fly on a level course without constantly adjusting for Earth's supposed curvature. These observable facts strongly support our position."
        }
    ]
}
```

#### Continuing a Conversation

**Request:**
```json
{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "But what about satellite images showing Earth as a sphere?"
}
```

**Response:**
```json
{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": [
        {
            "role": "user",
            "message": "I believe the Earth is flat and I can prove it"
        },
        {
            "role": "bot",
            "message": "Absolutely! The evidence for a flat Earth is compelling..."
        },
        {
            "role": "user",
            "message": "But what about satellite images showing Earth as a sphere?"
        },
        {
            "role": "bot",
            "message": "An excellent question that deserves scrutiny! Those images are actually CGI composites created by space agencies - they openly admit this. Real high-altitude footage from independent balloons shows a flat horizon at eye level, exactly as we'd expect on a flat plane..."
        }
    ]
}
```

### Response Format

- **conversation_id**: Unique identifier for the conversation (UUID format)
- **message**: Array of the last 5 message pairs (up to 10 messages total)
  - Each message has a `role` ("user" or "bot") and the message `message`
  - Messages are ordered chronologically (most recent last)

### Error Responses

**404 Not Found** - Conversation doesn't exist or expired:
```json
{
    "detail": "Conversation 550e8400-e29b-41d4-a716-446655440000 not found or expired"
}
```

**422 Validation Error** - Invalid request format:
```json
{
    "detail": [
        {
            "loc": ["body", "message"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

## 🛠️ Makefile Commands

The project includes a comprehensive Makefile with all required commands:

```bash
make              # Show all available commands
make install      # Install all requirements (checks Docker, creates .env)
make test         # Run the test suite
make run          # Build and run the service in Docker
make down         # Stop all running services
make clean        # Complete teardown and cleanup
```

Additional useful commands:

```bash
make build        # Build Docker images without starting
make logs         # View service logs in real-time
make status       # Show container status
make shell        # Open a shell in the running container
```

Development commands (for local development without Docker):

```bash
make dev-install  # Install dependencies locally
make dev-run      # Run locally with hot reload
make dev-test     # Run tests locally
```

## ⚙️ Environment Variables

All configuration is managed through environment variables in the `.env` file:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |

### Optional Variables (with defaults)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_MODEL` | OpenRouter model to use | `meta-llama/llama-3.1-8b-instruct` |
| `OPENAI_TEMPERATURE` | Response creativity (0.0-2.0) | `0.8` |
| `OPENAI_MAX_TOKENS` | Max tokens per response | `500` |
| `API_HOST` | API host address | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `MAX_HISTORY_MESSAGES` | Message pairs to return | `5` |
| `CONVERSATION_TIMEOUT_SECONDS` | Conversation expiry time | `3600` (1 hour) |

## 🧪 Testing

The project includes comprehensive tests covering:

- ✅ Health check and root endpoints
- ✅ New conversation creation
- ✅ Conversation continuation
- ✅ Invalid conversation handling
- ✅ Message validation
- ✅ Message history limits
- ✅ Multiple concurrent conversations

Run tests with:

```bash
make test
```

For local testing with coverage report:

```bash
make dev-test
```

## 🏗️ Architecture

### Project Structure

```
Kopi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── conversation.py     # Conversation management
│       └── debate_bot.py       # AI debate logic
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Test suite
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Service orchestration
├── Makefile                     # Build automation
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Design Decisions

#### 1. **Technology Stack**
- **FastAPI**: Modern, fast, with automatic API documentation and async support
- **OpenRouter AI**: Access to multiple AI models for persuasive, coherent responses
- **Pydantic**: Type safety and validation
- **Docker**: Consistent deployment environment
- **Pytest**: Comprehensive testing framework

#### 2. **In-Memory Storage**
- Conversations stored in memory for simplicity and speed
- Automatic cleanup of expired conversations
- For production at scale, could migrate to Redis or database

#### 3. **Conversation Management**
- Each conversation has unique UUID
- Maintains full history but returns only last 5 message pairs
- 1-hour timeout for inactive conversations

#### 4. **Debate Strategy**
- System prompt engineered to maintain position persuasively
- Temperature set to 0.8 for creative but coherent responses
- Max tokens limited to ensure sub-30-second responses
- Fallback responses if API fails

#### 5. **Error Handling**
- Proper HTTP status codes
- Validation on all inputs
- Graceful degradation with fallback responses

#### 6. **Testing Strategy**
- Unit tests with mocked OpenRouter API (to avoid costs/latency)
- Integration tests for full API flow
- Test coverage for edge cases

## 🔄 Example Usage

### Using cURL

```bash
# Start a new conversation
curl -X POST http://localhost:8000/api/v1/debate \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": null,
    "message": "Climate change is a hoax created by scientists"
  }'

# Continue the conversation (replace with actual conversation_id)
curl -X POST http://localhost:8000/api/v1/debate \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What about the melting ice caps?"
  }'
```

### Using Python

```python
import requests

# Start new conversation
response = requests.post(
    "http://localhost:8000/api/v1/debate",
    json={
        "conversation_id": None,
        "message": "Vaccines cause autism"
    }
)

data = response.json()
conversation_id = data["conversation_id"]
print(f"Bot: {data['message'][-1]['message']}")

# Continue conversation
response = requests.post(
    "http://localhost:8000/api/v1/debate",
    json={
        "conversation_id": conversation_id,
        "message": "But multiple studies disprove this"
    }
)

data = response.json()
print(f"Bot: {data['message'][-1]['message']}")
```

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Click on `POST /api/v1/debate`
3. Click "Try it out"
4. Enter your request JSON
5. Click "Execute"

## 🚀 Deployment

### Local Deployment

```bash
make run
```

### Production Deployment

The application is currently hosted on **Railway** for production deployment. Railway provides:

- **Automatic deployments** from GitHub
- **Environment variable management**
- **Built-in monitoring and logging**
- **Automatic scaling**
- **Custom domains support**

For production deployment, consider:

1. **Use environment-specific .env files**
2. **Add authentication/rate limiting**
3. **Use Redis for conversation storage**
4. **Add monitoring and logging (e.g., Sentry, DataDog)**
5. **Deploy behind a reverse proxy (Nginx)**
6. **Use managed container service (ECS, GKE, Cloud Run, Railway)**

Example docker-compose override for production:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  api:
    restart: always
    environment:
      - WORKERS=4
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 🔍 Troubleshooting

### Service won't start

```bash
# Check Docker is running
docker ps

# Check logs
make logs

# Verify .env file
cat .env | grep OPENAI_API_KEY
```

### API returns 500 errors

- Verify OpenRouter API key is valid
- Check API key has sufficient credits
- Review logs: `make logs`

### Tests failing

```bash
# Ensure dependencies are installed
make install

# Run tests with verbose output
make test
```

### Port 8000 already in use

Edit `.env` and change `API_PORT`:
```
API_PORT=8001
```

Then restart:
```bash
make down
make run
```

## 📝 License

This project is created as a coding challenge submission.

## 👤 Author

Built with professional standards following the Kopi Challenge requirements.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenRouter](https://openrouter.ai/) - AI model access platform
- [Railway](https://railway.app/) - Cloud deployment platform
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

---

**Note**: This bot will argue any position convincingly, including scientifically disproven theories. It's designed to demonstrate persuasive conversation capabilities, not to spread misinformation. Use responsibly! 🎯


