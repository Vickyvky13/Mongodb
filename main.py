from pyrogram import Client
from bot.handlers import start_handler, backup_handler
import config

# Initialize the bot
app = Client(
    "MongoBackupBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Add command handlers
@app.on_message(filters.command("start"))
async def start(client, message):
    await start_handler(client, message)

@app.on_message(filters.command("backup"))
async def backup(client, message):
    await backup_handler(client, message)

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
