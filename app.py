import os
import logging
from flask import Flask, request, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from bot import TelegramBot

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Telegram bot
telegram_bot = TelegramBot()

@app.route('/')
def index():
    """Home page showing bot status"""
    try:
        bot_info = telegram_bot.get_bot_info()
        status = "Online" if bot_info else "Offline"
        return render_template('index.html', 
                             bot_info=bot_info, 
                             status=status,
                             webhook_url=telegram_bot.webhook_url)
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return render_template('index.html', 
                             bot_info=None, 
                             status="Error",
                             webhook_url="Not set")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram updates"""
    try:
        if request.method == 'POST':
            # Get the JSON data from Telegram
            update_data = request.get_json()
            
            if update_data:
                logger.debug(f"Received update: {update_data}")
                # Process the update
                telegram_bot.process_update(update_data)
                return 'OK', 200
            else:
                logger.warning("Received empty update")
                return 'No data', 400
                
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return 'Error', 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'bot': 'running'}, 200

@app.route('/set_webhook')
def set_webhook():
    """Manually set webhook (for debugging)"""
    try:
        result = telegram_bot.set_webhook()
        if result:
            return {'status': 'success', 'message': 'Webhook set successfully'}
        else:
            return {'status': 'error', 'message': 'Failed to set webhook'}
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    # Set webhook on startup
    try:
        telegram_bot.set_webhook()
        logger.info("Webhook set successfully")
    except Exception as e:
        logger.error(f"Failed to set webhook on startup: {e}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
