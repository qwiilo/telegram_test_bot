import os
import logging
import requests
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.webhook_url = os.getenv('WEBHOOK_URL', '')
        
        logger.info(f"Bot initialized with token: {self.token[:10]}...")

    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Get bot information from Telegram API"""
        try:
            response = requests.get(f"{self.api_url}/getMe", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    return data.get('result')
            return None
        except Exception as e:
            logger.error(f"Error getting bot info: {e}")
            return None

    def set_webhook(self) -> bool:
        """Set webhook URL for the bot"""
        if not self.webhook_url:
            logger.error("WEBHOOK_URL environment variable is required")
            return False
        
        try:
            webhook_endpoint = f"{self.webhook_url}/webhook"
            data = {'url': webhook_endpoint}
            
            response = requests.post(f"{self.api_url}/setWebhook", 
                                   data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info(f"Webhook set successfully to: {webhook_endpoint}")
                    return True
                else:
                    logger.error(f"Failed to set webhook: {result.get('description')}")
            return False
            
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")
            return False

    def send_message(self, chat_id: int, text: str, 
                    parse_mode: str = 'HTML') -> bool:
        """Send a message to a chat"""
        try:
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            response = requests.post(f"{self.api_url}/sendMessage", 
                                   data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('ok', False)
            return False
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def process_update(self, update_data: Dict[str, Any]) -> None:
        """Process incoming update from Telegram"""
        try:
            # Handle regular messages
            if 'message' in update_data:
                message = update_data['message']
                self.handle_message(message)
            
            # Handle callback queries (inline keyboard presses)
            elif 'callback_query' in update_data:
                callback_query = update_data['callback_query']
                self.handle_callback_query(callback_query)
                
        except Exception as e:
            logger.error(f"Error processing update: {e}")

    def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming message"""
        try:
            chat_id = message['chat']['id']
            text = message.get('text', '')
            user = message.get('from', {})
            
            logger.info(f"Message from {user.get('username', 'Unknown')}: {text}")
            
            # Handle commands
            if text.startswith('/'):
                self.handle_command(chat_id, text, user)
            else:
                # Handle regular text messages
                self.handle_text_message(chat_id, text, user)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    def handle_command(self, chat_id: int, command: str, user: Dict[str, Any]) -> None:
        """Handle bot commands"""
        try:
            command = command.lower().split()[0]  # Get first word and make lowercase
            
            if command == '/start':
                welcome_text = f"""
🤖 <b>Welcome to the 24/7 Bot!</b>

Hello {user.get('first_name', 'there')}! 👋

This bot is running 24/7 using webhook architecture for maximum uptime and efficiency.

<b>Available Commands:</b>
/start - Show this welcome message
/help - Get help and information
/status - Check bot status
/ping - Test bot responsiveness

The bot is always online and ready to respond!
"""
                self.send_message(chat_id, welcome_text)
                
            elif command == '/help':
                help_text = """
<b>🆘 Help & Information</b>

<b>About this bot:</b>
• Runs 24/7 with webhook architecture
• Cost-effective alternative to expensive hosting
• Minimal resource usage for maximum uptime

<b>Commands:</b>
• /start - Welcome message
• /help - This help message
• /status - Bot status information
• /ping - Quick response test

<b>Features:</b>
✅ Always online
✅ Fast response times
✅ Reliable message handling
✅ Error recovery
✅ Detailed logging

Need more help? The bot automatically handles errors and stays responsive!
"""
                self.send_message(chat_id, help_text)
                
            elif command == '/status':
                bot_info = self.get_bot_info()
                if bot_info:
                    status_text = f"""
<b>🔧 Bot Status</b>

<b>Bot Information:</b>
• Name: {bot_info.get('first_name', 'Unknown')}
• Username: @{bot_info.get('username', 'Unknown')}
• ID: {bot_info.get('id', 'Unknown')}

<b>System Status:</b>
✅ Webhook: Active
✅ API: Connected
✅ Status: Online
✅ Uptime: 24/7

<b>Architecture:</b>
• Method: Webhook (not polling)
• Host: 0.0.0.0:5000
• Response: Real-time

The bot is running optimally! 🚀
"""
                else:
                    status_text = "❌ Unable to retrieve bot status. Please try again."
                
                self.send_message(chat_id, status_text)
                
            elif command == '/ping':
                ping_text = """
🏓 <b>Pong!</b>

✅ Bot is responsive and online
⚡ Response time: Instant
🌐 Connection: Stable

The bot is working perfectly! 
"""
                self.send_message(chat_id, ping_text)
                
            else:
                unknown_text = f"""
❓ <b>Unknown Command</b>

I don't recognize the command: <code>{command}</code>

<b>Available commands:</b>
/start - Welcome message
/help - Help and information
/status - Bot status
/ping - Test responsiveness

Type /help for more information!
"""
                self.send_message(chat_id, unknown_text)
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            error_text = "⚠️ An error occurred while processing your command. Please try again."
            self.send_message(chat_id, error_text)

    def handle_text_message(self, chat_id: int, text: str, user: Dict[str, Any]) -> None:
        """Handle regular text messages"""
        try:
            # Simple echo with helpful information
            response_text = f"""
💬 <b>Message Received!</b>

You said: <i>"{text}"</i>

This bot is designed for 24/7 uptime using webhook architecture. 

<b>Try these commands:</b>
/help - Get help
/status - Check bot status
/ping - Test responsiveness

The bot is always listening! 🤖
"""
            self.send_message(chat_id, response_text)
            
        except Exception as e:
            logger.error(f"Error handling text message: {e}")

    def handle_callback_query(self, callback_query: Dict[str, Any]) -> None:
        """Handle callback queries from inline keyboards"""
        try:
            # For future inline keyboard functionality
            query_id = callback_query['id']
            chat_id = callback_query['message']['chat']['id']
            
            # Answer the callback query to remove loading state
            requests.post(f"{self.api_url}/answerCallbackQuery", 
                         data={'callback_query_id': query_id})
            
        except Exception as e:
            logger.error(f"Error handling callback query: {e}")
