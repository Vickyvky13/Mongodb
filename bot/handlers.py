import os
import logging
from pyrogram import Client, filters
from bot.repository import BackupRepository
import config

# Setup logging
logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

async def start_handler(client, message):
    await message.reply_text("Hello! Send /backup to back up your MongoDB databases (bot owner only).")

async def backup_handler(client, message):
    # Check if the sender is the bot owner
    if message.from_user.id != config.BOT_OWNER_ID:
        await message.reply_text("You are not authorized to perform this action.")
        return

    await message.reply_text("Starting the backup process...")
    logging.info("Backup process initiated by the bot owner.")

    backup_files = []
    for db_name, uri in config.MONGO_URIS.items():
        repo = BackupRepository(uri, db_name, config.BACKUP_DIR)
        backup_file = repo.backup()

        if backup_file:
            backup_files.append(backup_file)
            await client.send_document(
                chat_id=config.LOG_GROUP_ID,  # Send to the group
                document=backup_file,
                caption=f"Backup completed for {db_name}.",
            )
            logging.info(f"Backup completed for {db_name}: {backup_file}")
            os.remove(backup_file)  # Cleanup after sending
        else:
            logging.error(f"Backup failed for {db_name}")
            await client.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"Backup failed for {db_name}.",
            )

    if backup_files:
        await client.send_message(
            chat_id=config.LOG_GROUP_ID,
            text="All backups have been completed and sent to this group.",
        )
    else:
        await client.send_message(
            chat_id=config.LOG_GROUP_ID,
            text="No backups were created.",
        )

    # Send the backup log file to the group
    if os.path.exists("backup.log"):
        await client.send_document(
            chat_id=config.LOG_GROUP_ID,
            document="backup.log",
            caption="Backup process log file.",
      )
