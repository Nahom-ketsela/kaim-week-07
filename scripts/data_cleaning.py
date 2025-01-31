import pandas as pd
import logging
import os
import re
import emoji


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/data_cleaning.log", encoding="utf-8"),  # Ensure UTF-8 encoding
        logging.StreamHandler()
    ]
)

# Function to load a csv file 
def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}")
        raise

def extract_emojis(text):
    """ Extract emojis from text, return 'No emoji' if none found. """
    emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
    return emojis if emojis else "No emoji"

def remove_emojis(text):
    """ Remove emojis from the message text. """
    return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

def extract_youtube_links(text):
    """ Extract YouTube links from text, return 'No YouTube link' if none found. """
    youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    links = re.findall(youtube_pattern, text)
    return ', '.join(links) if links else "No YouTube link"

def remove_youtube_links(text):
    """ Remove YouTube links from the message text. """
    youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
    return re.sub(youtube_pattern, '', text).strip()

def clean_text(text):
    """ Standardize text by removing newline characters and unnecessary spaces. """
    if pd.isna(text):
        return "No Message"
    return re.sub(r'\n+', ' ', text).strip()


def clean_dataframe(df):
    """ Perform all cleaning and standardization steps. """
    try:
        df = df.drop_duplicates().copy()
        logging.info("✅ Duplicates removed.")
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date'] = df['date'].where(df['date'].notna(), None)
            logging.info("✅ Date column formatted.")
        
        if 'id' in df.columns:
            df['id'] = pd.to_numeric(df['id'], errors="coerce").fillna(0).astype(int)
            logging.info("✅ ID column standardized.")
        
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
            logging.info(f"✅ Column '{col}' standardized.")
        
        df = df.fillna(method='ffill').fillna(method='bfill')
        logging.info("✅ Missing values handled.")
        
        if 'message' in df.columns:
            df['emoji_used'] = df['message'].apply(extract_emojis)
            df['message'] = df['message'].apply(remove_emojis)
            df['youtube_links'] = df['message'].apply(extract_youtube_links)
            df['message'] = df['message'].apply(remove_youtube_links)
            df['message'] = df['message'].apply(clean_text)
            logging.info("✅ Emoji and YouTube link processing completed.")
        
        df = df.rename(columns=lambda x: x.lower().replace(" ", "_"))
        logging.info("✅ Columns renamed for consistency.")
        
        logging.info("✅ Data cleaning completed successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Data cleaning error: {e}")
        raise

def save_cleaned_data(df, output_path):
    """ Save cleaned data to a new CSV file. """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned data saved to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving cleaned data: {e}")
        raise

