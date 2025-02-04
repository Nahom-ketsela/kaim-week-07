import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging to write to file & display in terminal/Jupyter
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/database_setup.log"),  # Log to file
        logging.StreamHandler()  # Log to  Jupyter
    ]
)

# Load environment variables
load_dotenv("../.env")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """
    Create and return database engine using credentials from .env.
    """
    try:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL)

        # Test the connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logging.info("Successfully connected to the PostgreSQL database.")

        return engine
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def drop_table(engine):
    """
    Drop the 'detections' table if it exists.
    """
    drop_table_query = """
    DROP TABLE IF EXISTS detections;
    """
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(drop_table_query))
        logging.info("Table 'detections' dropped successfully.")
    except Exception as e:
        logging.error(f" Error dropping table: {e}")
        raise

def create_table(engine):
    """
    Create the 'detections' table if it does not exist.
    This schema corresponds to the CSV columns: 
    image_name, class_id, x_center, y_center, width, height, confidence
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS detections (
        id SERIAL PRIMARY KEY,
        image_name TEXT,
        class_id INT,
        x_center DOUBLE PRECISION,
        y_center DOUBLE PRECISION,
        width DOUBLE PRECISION,
        height DOUBLE PRECISION,
        confidence DOUBLE PRECISION
    );
    """
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(create_table_query))
        logging.info(" Table 'detections' created successfully.")
    except Exception as e:
        logging.error(f" Error creating table: {e}")
        raise

def insert_data(engine, csv_file_path):
    """
    Insert detection data from the specified CSV file into the 'detections' table.
    The CSV is expected to have columns:
        image_name, class_id, x_center, y_center, width, height, confidence
    """
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_file_path)
        logging.info(f"Loading data from: {csv_file_path}")
        logging.info(f"Dataframe shape: {df.shape}")

        insert_query = """
        INSERT INTO detections 
            (image_name, class_id, x_center, y_center, width, height, confidence)
        VALUES 
            (:image_name, :class_id, :x_center, :y_center, :width, :height, :confidence)
        """

        # Insert records in a transaction
        with engine.begin() as connection:
            for _, row in df.iterrows():
                connection.execute(
                    text(insert_query),
                    {
                        "image_name": row["image_name"],
                        "class_id": row["class_id"],
                        "x_center": row["x_center"],
                        "y_center": row["y_center"],
                        "width": row["width"],
                        "height": row["height"],
                        "confidence": row["confidence"]
                    }
                )

        logging.info(f" {len(df)} records inserted into 'detections' table.")
    except Exception as e:
        logging.error(f" Error inserting data into 'detections': {e}")
        raise

