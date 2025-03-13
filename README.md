# Ethiopian Medical Business Data Warehouse

This project is a comprehensive data engineering solution designed to collect, clean, transform, and store data related to Ethiopian medical businesses. It scrapes data from public Telegram channels, processes it using advanced techniques like object detection with YOLO, and stores it in a centralized data warehouse. The data is exposed via a FastAPI application for easy access and analysis.

---

## 🚀 Key Features

- **Automated Telegram Data Scraping**: Collects text and image data from public Telegram channels.
- **Data Cleaning & Transformation**: Cleans and standardizes data for consistency and usability.
- **Object Detection with YOLO**: Extracts insights from images using state-of-the-art object detection.
- **Centralized Data Storage**: Stores processed data in a PostgreSQL database for efficient querying.
- **API Access**: Exposes data via a FastAPI application for easy integration and retrieval.
- **Scalable Design**: Built to handle large volumes of data and extendable for additional sources.
- **Interactive Exploration**: Includes Jupyter Notebooks for step-by-step data analysis.

---

## 🛠 Project Structure

```
WEEK7/
│── data/                          # Raw and cleaned data storage
│   ├── images
│   ├── raw_telegram_data.csv
│   ├── yolo_detections.csv
│   ├── cleaned_telegram_data.csv  # Cleaned merged dataset
│── logs/                          # Logging directory
│── FasrApi/                      # FastApi for the backend
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schema.py
│── Frontend/                      # React.js for the frontend
│── notebook/                      # Jupyter Notebooks for analysis
│   ├── data_cleaning.ipynb
|   ├── load_yolov5_to_db.ipynb
|   ├── Object_detection_using_yolo.ipynb
│── scripts/                       # Python scripts for processing
│   ├── data_cleaning.py           # Functions for data cleaning
│   ├── database_connection.py          # Database connection and table creation
│   ├── telegram_scraper.py            # Telegram data scraper
│── telegram_message_dbt/          # dbt (Data build tools)
│── test/                       # Python scripts for testing (unit test)
│   ├── test_data_cleaning.py  
│── .env                           # Environment variables
│── .gitignore                     # Files to ignore in version control
│── channels.json                  # List of Telegram channels
│── requirements.txt                
│── README.md                      # Project documentation
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.8+
- PostgreSQL
- Telegram API credentials

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd <repository-folder>
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```plaintext
   DB_NAME=your_database
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432

   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   ```

### Running the Project
1. **Scrape Data from Telegram**:
   ```bash
   python scripts/telegram_scraper.py
   ```
2. **Clean the Data**:
   ```bash
   python scripts/data_cleaning.py
   ```
3. **Store Data in Database**:
   ```bash
   python scripts/database_connection.py
   ```
4. **Start FastAPI Server** (Optional):
   ```bash
   uvicorn main:app --reload
   ```
   Access the API at `http://127.0.0.1:8000`.

5. **Explore Data with Jupyter Notebook**:
   ```bash
   jupyter notebook notebook/data_cleaning.ipynb
   ```

---

## 📞 Contact & Support
For issues or questions nahoket@gmail.com.

---

## 📌 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 

Enjoy exploring the Ethiopian medical business data! 🚀
