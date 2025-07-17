# Overview

This repository contains a Flask-based Telegram bot application designed for 24/7 operation using webhook architecture. The bot is built to be cost-effective and maintain maximum uptime by leveraging webhooks instead of polling for updates.

# System Architecture

The application follows a simple yet effective architecture:

- **Frontend**: Basic HTML template with Bootstrap for displaying bot status
- **Backend**: Flask web server with webhook endpoint for receiving Telegram updates
- **Bot Logic**: Custom TelegramBot class handling API communication and update processing
- **Deployment**: Designed for cloud hosting platforms with webhook support

The webhook-based approach was chosen over polling to reduce resource consumption and improve response times, making it ideal for 24/7 operation on platforms like Replit.

# Key Components

## Flask Application (`app.py`)
- Main web server handling HTTP requests
- Home route for bot status display
- Webhook endpoint for receiving Telegram updates
- Configured with ProxyFix middleware for proper header handling behind proxies
- Comprehensive logging for debugging and monitoring

## Telegram Bot Class (`bot.py`)
- Handles all Telegram API interactions
- Manages webhook configuration
- Processes incoming updates from Telegram
- Includes error handling and logging for reliability

## Web Interface (`templates/index.html`)
- Bootstrap-based dark theme interface
- Real-time bot status display
- Shows bot information and webhook configuration
- Responsive design for mobile and desktop viewing

## Entry Point (`main.py`)
- Simple application entry point importing the Flask app

# Data Flow

1. **Incoming Updates**: Telegram sends POST requests to `/webhook` endpoint when users interact with the bot
2. **Processing**: Flask receives the webhook data and passes it to the TelegramBot class
3. **Response**: Bot processes the update and can send responses back to Telegram via API calls
4. **Status Monitoring**: Home page displays current bot status by querying Telegram API

# External Dependencies

## Required Environment Variables
- `TELEGRAM_BOT_TOKEN`: Bot token from BotFather (required)
- `WEBHOOK_URL`: Public URL where the bot is hosted (required for webhook setup)
- `SESSION_SECRET`: Flask session secret (optional, has fallback)

## Python Packages
- `flask`: Web framework for handling HTTP requests
- `requests`: HTTP client for Telegram API communication
- `werkzeug`: WSGI utilities (ProxyFix middleware)

## External Services
- **Telegram Bot API**: Primary integration for bot functionality
- **Bootstrap CDN**: Frontend styling and components
- **Font Awesome CDN**: Icons for the web interface

# Deployment Strategy

The application is designed for deployment on cloud platforms that support:
- Python/Flask applications
- Environment variable configuration
- Public webhook URLs
- 24/7 uptime capabilities

Key deployment considerations:
- Webhook URL must be publicly accessible and use HTTPS
- Environment variables must be properly configured
- Application should restart automatically on failures
- Logging is configured for monitoring and debugging

# Changelog

- July 04, 2025. Initial setup

# User Preferences

Preferred communication style: Simple, everyday language.