import unittest
import pandas as pd
from io import StringIO
import os
import logging

# Adjust the import path for functions from data cleaning
from scripts.data_cleaning import load_csv, extract_emojis, remove_emojis, extract_youtube_links, remove_youtube_links, clean_text, clean_dataframe, save_cleaned_data

class TestDataCleaning(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a temporary log file or adjust if needed
        os.makedirs("../logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("../logs/test_data_cleaning.log", encoding='utf-8')]
        )

    def setUp(self):
        # Create a mock CSV content to load into the DataFrame for testing
        self.csv_data = StringIO(""" 
        message_id,date,text,channel,sender_id,image_path
        1,2023-03-01,Hello! 😊 https://youtube.com/watch?v=dQw4w9WgXcQ,#test_channel,101,images/img1.jpg
        2,2023-03-02,How are you? No link, no emoji.,#test_channel,102,images/img2.jpg
        3,2023-03-03,Goodbye! 🎉 https://youtu.be/abc1234,#test_channel,103,images/img3.jpg
        4,2023-03-04,Test message without emoji or link,#test_channel,104,images/img4.jpg
        """)
        self.df = pd.read_csv(self.csv_data)

    def test_load_csv(self):
        """Test loading of CSV files."""
        # Adjust file path as needed for your test
        df = load_csv("../data/cleaned_telegram_data.csv")
        self.assertIsInstance(df, pd.DataFrame, "Data should be loaded as a pandas DataFrame.")

    def test_extract_emojis(self):
        """Test extracting emojis from a text."""
        result = extract_emojis("Hello! 😊")
        self.assertEqual(result, "😊", "Emojis should be extracted correctly.")
        result_no_emoji = extract_emojis("No emoji here!")
        self.assertEqual(result_no_emoji, "No emoji", "Should return 'No emoji' if no emoji present.")

    def test_remove_emojis(self):
        """Test removing emojis from a text."""
        result = remove_emojis("Hello! 😊")
        self.assertEqual(result, "Hello! ", "Emojis should be removed correctly.")
        result_no_emoji = remove_emojis("No emoji here!")
        self.assertEqual(result_no_emoji, "No emoji here!", "Should return text unchanged if no emoji present.")

    def test_extract_youtube_links(self):
        """Test extracting YouTube links from a text."""
        result = extract_youtube_links("Check this out: https://youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(result, "https://youtube.com/watch?v=dQw4w9WgXcQ", "YouTube link should be extracted correctly.")
        result_no_link = extract_youtube_links("No link here!")
        self.assertEqual(result_no_link, "No YouTube link", "Should return 'No YouTube link' if no link present.")

    def test_remove_youtube_links(self):
        """Test removing YouTube links from a text."""
        result = remove_youtube_links("Check this out: https://youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(result, "Check this out: ", "YouTube link should be removed correctly.")
        result_no_link = remove_youtube_links("No link here!")
        self.assertEqual(result_no_link, "No link here!", "Should return text unchanged if no link present.")

    def test_clean_text(self):
        """Test cleaning of text."""
        result = clean_text("This is a test message.\n")
        self.assertEqual(result, "This is a test message.", "Newline characters should be removed.")
        result_no_newline = clean_text("No newline here.")
        self.assertEqual(result_no_newline, "No newline here.", "Text without newline should remain unchanged.")

    def test_clean_dataframe(self):
        """Test cleaning of DataFrame."""
        cleaned_df = clean_dataframe(self.df)
        # Ensure the dataframe is cleaned correctly
        self.assertIn("emoji_used", cleaned_df.columns, "Should have an 'emoji_used' column.")
        self.assertIn("youtube_links", cleaned_df.columns, "Should have a 'youtube_links' column.")
        self.assertEqual(cleaned_df.shape[0], 4, "Number of rows should remain the same after cleaning.")
        self.assertEqual(cleaned_df['message'].iloc[0], "Hello! ", "Emojis should be removed from 'message'.")

    def test_save_cleaned_data(self):
        """Test saving cleaned DataFrame to CSV."""
        cleaned_df = clean_dataframe(self.df)
        output_path = "../logs/test_cleaned_data.csv"
        save_cleaned_data(cleaned_df, output_path)
        self.assertTrue(os.path.exists(output_path), f"Saved file should exist at {output_path}")
        os.remove(output_path)  # Clean up after the test

    @classmethod
    def tearDownClass(cls):
        # Clean up logs if necessary
        log_file = "../logs/test_data_cleaning.log"
        if os.path.exists(log_file):
            os.remove(log_file)


if __name__ == "__main__":
    unittest.main()
