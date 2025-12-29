#!/bin/bash
# CloudWalk Helper - One-Command Start Script for Linux/Mac
# This script sets up and runs the CloudWalk Helper chatbot

echo ""
echo "========================================"
echo " CloudWalk Helper - Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed."
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running."
    echo "Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available (either standalone or as docker plugin)
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "[ERROR] docker-compose is not installed."
    exit 1
fi

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    echo "[INFO] Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ""
        echo "[IMPORTANT] Please edit .env file and add your OpenRouter API key!"
        echo "Get a free key at: https://openrouter.ai"
        echo ""
        echo "Edit .env with your preferred editor, then run this script again."
        
        # Try to open with default editor
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo "Please edit .env manually and run this script again."
            exit 0
        fi
    else
        echo "[ERROR] .env.example not found!"
        exit 1
    fi
fi

echo "[INFO] Building and starting CloudWalk Helper..."
echo "This may take a few minutes on first run..."
echo ""

# Build and run with Docker Compose
$COMPOSE_CMD up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo " CloudWalk Helper is running!"
    echo "========================================"
    echo ""
    echo " Open your browser at:"
    echo " http://localhost:8501"
    echo ""
    echo " To stop: $COMPOSE_CMD down"
    echo "========================================"
    echo ""
    
    # Try to open browser automatically
    sleep 3
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8501
    elif command -v open &> /dev/null; then
        open http://localhost:8501
    fi
else
    echo "[ERROR] Failed to start. Check the logs above."
    exit 1
fi
