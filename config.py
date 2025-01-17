import os

# Telegram Bot Config
API_ID = os.getenv("API_ID", "your_api_id")
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# MongoDB URIs and backup directory
MONGO_URIS = {
    "FBot": os.getenv("MONGODB_URI_1", "mongodb+srv://user:pass@cluster0.mongodb.net/FBot"),
    "ChatGPTBot": os.getenv("MONGODB_URI_2", "mongodb+srv://user:pass@cluster0.mongodb.net/ChatGPTBot"),
}

# Backup directory
BACKUP_DIR = "./backups"

# Bot owner ID and group ID for logs
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "123456789"))  # Replace with your Telegram ID
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-987654321"))  # Replace with your group ID
