# Root Makefile for multi-tenant quote app

PROJECT_NAME := multi-tenant-quote-app
COMPOSE_FILE := deploy/docker-compose.yml
DC := docker compose -f $(COMPOSE_FILE)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make build        Build all docker images"
	@echo "  make up           Start all services in background"
	@echo "  make up-dev       Start services with build (development)"
	@echo "  make down         Stop and remove containers, networks"
	@echo "  make restart      Restart all services"
	@echo "  make logs         Follow logs for all services"
	@echo "  make logs-backend Follow logs for backend service"
	@echo "  make logs-frontend Follow logs for frontend service"

.PHONY: build
build:
	$(DC) build

.PHONY: up
up:
	$(DC) up -d

.PHONY: up-dev
up-dev:
	$(DC) up -d --build

.PHONY: down
down:
	$(DC) down

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	$(DC) logs -f

.PHONY: logs-backend
logs-backend:
	$(DC) logs -f backend

.PHONY: logs-frontend
logs-frontend:
	$(DC) logs -f frontend
