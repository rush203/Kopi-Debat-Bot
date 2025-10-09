.PHONY: help install test run down clean build lint format check

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Kopi Debate Bot - Available Commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

check-docker: ## Check if Docker is installed
	@which docker > /dev/null || (echo "$(RED)Error: Docker is not installed.$(NC)" && \
		echo "$(YELLOW)Please install Docker from: https://docs.docker.com/get-docker/$(NC)" && exit 1)
	@which docker-compose > /dev/null || docker compose version > /dev/null || \
		(echo "$(RED)Error: Docker Compose is not installed.$(NC)" && \
		echo "$(YELLOW)Please install Docker Compose from: https://docs.docker.com/compose/install/$(NC)" && exit 1)
	@echo "$(GREEN)✓ Docker is installed$(NC)"

check-env: ## Check if .env file exists
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Warning: .env file not found. Creating from .env.example...$(NC)"; \
		cp .env.example .env; \
		echo "$(RED)Important: Please edit .env and add your OPENAI_API_KEY$(NC)"; \
		exit 1; \
	fi
	@if grep -q "your_openai_api_key_here" .env; then \
		echo "$(RED)Error: Please set your OPENAI_API_KEY in the .env file$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Environment configuration is valid$(NC)"

install: check-docker ## Install all requirements and dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env file from .env.example...$(NC)"; \
		cp .env.example .env; \
		echo "$(RED)Important: Edit .env and add your OPENAI_API_KEY before running the service$(NC)"; \
	fi
	@docker compose pull || docker-compose pull || true
	@echo "$(GREEN)✓ Installation complete$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Edit .env and add your OPENAI_API_KEY"
	@echo "  2. Run 'make run' to start the service"

build: check-docker ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker compose build || docker-compose build
	@echo "$(GREEN)✓ Build complete$(NC)"

test: check-docker check-env ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	@docker compose run --rm api pytest tests/ -v || \
		docker-compose run --rm api pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"

run: check-docker check-env ## Run the service in Docker
	@echo "$(BLUE)Starting Kopi Debate Bot...$(NC)"
	@docker compose up -d --build || docker-compose up -d --build
	@echo "$(GREEN)✓ Service started successfully$(NC)"
	@echo ""
	@echo "$(GREEN)API is running at: http://localhost:8000$(NC)"
	@echo "$(GREEN)API Documentation: http://localhost:8000/docs$(NC)"
	@echo "$(GREEN)Health Check: http://localhost:8000/api/v1/health$(NC)"
	@echo ""
	@echo "$(YELLOW)View logs:$(NC) make logs"
	@echo "$(YELLOW)Stop service:$(NC) make down"

logs: ## Show service logs
	@docker compose logs -f api || docker-compose logs -f api

down: check-docker ## Stop all running services
	@echo "$(BLUE)Stopping services...$(NC)"
	@docker compose down || docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

clean: check-docker ## Stop and remove all containers, networks, and volumes
	@echo "$(BLUE)Cleaning up...$(NC)"
	@docker compose down -v --remove-orphans || docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

status: check-docker ## Show status of running containers
	@docker compose ps || docker-compose ps

shell: check-docker ## Open a shell in the running container
	@docker compose exec api /bin/bash || docker-compose exec api /bin/bash

lint: check-docker ## Run linting
	@echo "$(BLUE)Running linter...$(NC)"
	@docker compose run --rm api python -m py_compile app/**/*.py || \
		docker-compose run --rm api python -m py_compile app/**/*.py
	@echo "$(GREEN)✓ Lint complete$(NC)"

# Development targets (local, without Docker)
dev-install: ## Install dependencies locally for development
	@echo "$(BLUE)Installing Python dependencies locally...$(NC)"
	@pip install -r requirements.txt
	@echo "$(GREEN)✓ Local installation complete$(NC)"

dev-run: ## Run the service locally (without Docker)
	@echo "$(BLUE)Starting service locally...$(NC)"
	@uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-test: ## Run tests locally (without Docker)
	@echo "$(BLUE)Running tests locally...$(NC)"
	@pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"


