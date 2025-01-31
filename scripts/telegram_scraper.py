import os
import asyncio
import csv
import logging
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChannelInvalidError, FloodWaitError
from telethon.tl.types import MessageMediaPhoto

from dotenv import load_dotenv, find_dotenv


# Locate and Load .env

load_dotenv(find_dotenv())  # Automatically looks up the directory tree for .env

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Telegram channels
channels_to_scrape = ["DoctorsET", "lobelia4cosmetics", "yetenaweg", "EAHCI", "CheMed123", "pzeth"]

# Data storage
OUTPUT_FOLDER = os.path.join("..", "data")  # Go one directory up (relative to scripts/)
RAW_DATA_CSV = os.path.join(OUTPUT_FOLDER, "telegram_raw_data.csv")
IMAGES_FOLDER = os.path.join(OUTPUT_FOLDER, "images")


async def scrape_channel(client, channel_name, limit=500):
    logger.info(f"Scraping channel: {channel_name}")
    messages_data = []

    try:
        channel_image_folder = os.path.join(IMAGES_FOLDER, channel_name)
        os.makedirs(channel_image_folder, exist_ok=True)

        async for message in client.iter_messages(channel_name, limit=limit):
            message_id = message.id
            date = message.date
            sender_id = message.sender_id
            text = message.message if message.message else ""
            image_path = None

            # Download image
            if message.media and isinstance(message.media, MessageMediaPhoto):
                filename = f"{channel_name}_{message_id}.jpg"
                file_path = os.path.join(channel_image_folder, filename)
                try:
                    await message.download_media(file=file_path)
                    image_path = file_path
                except Exception as e:
                    logger.error(f"Error downloading image for message {message_id}: {e}")
                    image_path = None

            messages_data.append({
                "channel": channel_name,
                "message_id": message_id,
                "date": date.isoformat() if date else "",
                "sender_id": sender_id,
                "text": text,
                "image_path": image_path
            })

        logger.info(f"Completed scraping channel: {channel_name} - Total messages: {len(messages_data)}")

    except ChannelInvalidError:
        logger.error(f"Channel {channel_name} is invalid or you don't have access.")
    except FloodWaitError as e:
        logger.error(f"FloodWaitError - Telegram is blocking requests for {e.seconds} seconds. Script will pause.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.error(f"Unexpected error scraping channel {channel_name}: {e}")

    return messages_data


async def main():
    # Initialize client
    client = TelegramClient('session_name', API_ID, API_HASH)
    logger.info("Starting Telegram client...")
    await client.start(phone=PHONE_NUMBER)
    logger.info("Telegram client started successfully.")

    # Create folders if they don't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

    # Write CSV headers if file doesn't exist
    csv_headers = ["channel", "message_id", "date", "sender_id", "text", "image_path"]
    if not os.path.exists(RAW_DATA_CSV):
        with open(RAW_DATA_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)

    # Scrape channels
    all_messages = []
    for channel_name in channels_to_scrape:
        channel_messages = await scrape_channel(client, channel_name, limit=100)
        all_messages.extend(channel_messages)

    # Append data to CSV
    with open(RAW_DATA_CSV, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        for msg in all_messages:
            writer.writerow(msg)

    logger.info("Data successfully appended to CSV. Scraping completed.")
    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
