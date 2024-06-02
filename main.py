import os
import subprocess
from datetime import datetime
from pyrogram import Client, filters
from pymongo import MongoClient

# Telegram bot token and API details
API_ID = '12526414'
API_HASH = '78c6e4ddc726ef7a326d2439a379abb1'
BOT_TOKEN = '7362816875:AAH-xM6fHJfEKzoveQpIPGuBeWWJ8ymVT7k'

# MongoDB connection details
MONGO_URI = "mongodb+srv://shivanibaby528:15406578@cluster0.itxjmfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "your_database"

# Initialize Pyrogram Client
app = Client("mongodb_backup_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)

@app.on_message(filters.command("backup"))
async def backup(client, message):
    try:
        # Create a backup of the MongoDB database
        backup_file = f"{DATABASE_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gz"
        command = f"mongodump --uri={MONGO_URI}/{DATABASE_NAME} --archive={backup_file} --gzip"
        subprocess.run(command, shell=True, check=True)
        
        # Send the backup file to the user
        await app.send_document(message.chat.id, backup_file)
        
        # Clean up the backup file
        os.remove(backup_file)
        
        await message.reply("Backup completed and sent!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@app.on_message(filters.command("restore") & filters.document)
async def restore(client, message):
    try:
        # Download the backup file
        backup_file_path = await message.download()
        
        # Restore the MongoDB database from the backup file
        command = f"mongorestore --uri={MONGO_URI}/{DATABASE_NAME} --archive={backup_file_path} --gzip --drop"
        subprocess.run(command, shell=True, check=True)
        
        # Clean up the downloaded backup file
        os.remove(backup_file_path)
        
        await message.reply("Restore completed successfully!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

if __name__ == "__main__":
    app.run()
