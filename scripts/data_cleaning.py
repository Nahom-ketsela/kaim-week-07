import pandas as pd
import logging
import re
import os
import emoji
import traceback

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging to write to file & display in Jupyter Notebook
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_cleaning.log", encoding='utf-8'),  # Set encoding to utf-8
        logging.StreamHandler()  # Log to Jupyter Notebook output
    ]
)


def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}\n{traceback.format_exc()}")
        raise


def extract_emojis(text):
    """ Extract emojis from text, return 'No emoji' if none found. """
    if pd.isna(text) or text is None:
        return "No emoji"
    emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
    return emojis if emojis else "No emoji"


def remove_emojis(text):
    """ Remove emojis from the message text. """
    if pd.isna(text) or text is None:
        return text
    return ''.join(c for c in text if c not in emoji.EMOJI_DATA)


def extract_youtube_links(text):
    """ Extract YouTube links from text, return 'No YouTube link' if none found. """
    if pd.isna(text) or text is None:
        return "No YouTube link"
    youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    links = re.findall(youtube_pattern, text)
    return ', '.join(links) if links else "No YouTube link"


def remove_youtube_links(text):
    """ Remove YouTube links from the message text. """
    if pd.isna(text) or text is None:
        return text
    youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
    return re.sub(youtube_pattern, '', text).strip()


def clean_text(text):
    """ Standardize text by removing newline characters and unnecessary spaces. """
    if pd.isna(text) or text is None:
        return "No Message"
    return re.sub(r'\n+', ' ', str(text)).strip()


def clean_dataframe(df):
    """ Perform all cleaning and standardization steps while avoiding errors. """
    try:
        # Strip leading/trailing spaces from column names
        df.columns = df.columns.str.strip()

        # Drop duplicates if 'message_id' exists
        if 'message_id' in df.columns:
            df = df.drop_duplicates(subset=['message_id']).copy()
            logging.info("✅ Duplicates removed from dataset.")
        else:
            logging.warning("⚠️ 'message_id' column not found. Skipping duplicate removal.")

        # Convert 'date' to datetime format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date'] = df['date'].where(df['date'].notna(), None)
            logging.info("✅ Date column formatted to datetime.")
        else:
            logging.warning("⚠️ 'date' column not found. Skipping datetime conversion.")

        # Convert 'message_id' to integer if it exists
        if 'message_id' in df.columns:
            df['message_id'] = pd.to_numeric(df['message_id'], errors="coerce").fillna(0).astype(int)
        else:
            logging.warning("⚠️ 'message_id' column not found. Skipping integer conversion.")

        # Fill missing values for expected columns
        for col in ['text', 'image_path']:
            if col in df.columns:
                df[col] = df[col].fillna("No Data")
            else:
                logging.warning(f"⚠️ '{col}' column not found. Skipping missing value filling.")

        # Standardize text columns if they exist
        for col in ['channel', 'text', 'image_path']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            else:
                logging.warning(f"⚠️ '{col}' column not found. Skipping text standardization.")

        # Extract and remove emojis
        if 'text' in df.columns:
            df['emoji_used'] = df['text'].apply(extract_emojis)
            df['text'] = df['text'].apply(remove_emojis)
            logging.info("✅ Emojis processed.")
        else:
            logging.warning("⚠️ 'text' column not found. Skipping emoji processing.")

        # Extract and remove YouTube links
        if 'text' in df.columns:
            df['youtube_links'] = df['text'].apply(extract_youtube_links)
            df['text'] = df['text'].apply(remove_youtube_links)
            logging.info("✅ YouTube links processed.")
        else:
            logging.warning("⚠️ 'text' column not found. Skipping YouTube link processing.")

        # Remove newline characters from the 'text' column
        if 'text' in df.columns:
            df['text'] = df['text'].apply(clean_text)
            logging.info("✅ Newline characters removed from 'text' column.")
        else:
            logging.warning("⚠️ 'text' column not found. Skipping newline removal.")

        # Rename columns to match desired output
        rename_map = {
            "channel": "channel_username",
            "sender_id": "sender_id",  # Assuming 'sender_id' is the username
            "message_id": "message_id",
            "text": "message",
            "date": "message_date",
            "image_path": "media_path",
            "emoji_used": "emoji_used",
            "youtube_links": "youtube_links"
        }
        df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

        # Select only the desired columns
        desired_columns = [
            "channel_username", "sender_id", "message_id", "message",
            "message_date", "media_path", "emoji_used", "youtube_links"
        ]
        df = df[[col for col in desired_columns if col in df.columns]]

        logging.info("✅ Data cleaning completed successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Data cleaning error: {e}\n{traceback.format_exc()}")
        raise

def save_cleaned_data(df, output_path):
    """ Save cleaned data to a new CSV file. """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned data saved successfully to '{output_path}'.")
        print(f"✅ Cleaned data saved successfully to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving cleaned data: {e}\n{traceback.format_exc()}")
        raise

