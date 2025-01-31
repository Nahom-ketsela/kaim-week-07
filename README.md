# Ethiopian Medical Business Data Warehouse

## Overview

The **Ethiopian Medical Business Data Warehouse** is a comprehensive data engineering project designed to collect, clean, transform, and store data related to Ethiopian medical businesses. The data is primarily scraped from public Telegram channels, which serve as a rich source of information about medical products, services, and trends in Ethiopia. The project also incorporates **object detection** using YOLO (You Only Look Once) to analyze images scraped from these channels, enabling the extraction of valuable insights from visual data.

The processed data is stored in a centralized **data warehouse**, making it easily accessible for analysis and reporting. Additionally, the project exposes the collected data via a **FastAPI** application, providing a user-friendly interface for querying and retrieving information. This project is a powerful tool for businesses, researchers, and policymakers to gain insights into the Ethiopian medical sector, identify trends, and make data-driven decisions.

---

## What the Project Does

1. **Data Collection**:
   - The project scrapes data from public Telegram channels related to Ethiopian medical businesses. This includes text data (e.g., product descriptions, prices, and contact information) as well as images (e.g., product photos, advertisements).

2. **Data Cleaning and Transformation**:
   - The scraped data is cleaned and transformed to ensure consistency and usability. This involves removing duplicates, handling missing values, standardizing formats, and validating the data.

3. **Object Detection**:
   - Images scraped from Telegram channels are processed using **YOLO**, a state-of-the-art object detection model. This allows the project to identify and extract relevant objects (e.g., medical products) from the images, enriching the dataset with visual insights.

4. **Data Storage**:
   - The cleaned and transformed data is stored in a **data warehouse**, which serves as a centralized repository for all collected information. This enables efficient querying, reporting, and analysis.

5. **API Exposure**:
   - The project provides a **FastAPI** application to expose the collected data. This API allows users to query the data warehouse, retrieve specific information, and integrate the data into other applications or workflows.

---

## How to Run the Project

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (or any other SQL database)
- Telegram API credentials (for scraping)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <this repository link>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Create a PostgreSQL database and update the connection details in the `database_connection.py` file.

4. **Configure Telegram API**:
   - Obtain your Telegram API credentials and update the `telegram_scraper.py` script with your credentials.

### Running the Project

1. **Run the Data Scraper**:
   - Execute the Telegram scraper to collect data from the specified channels:
     ```bash
     python scripts/telegram_scraper.py
     ```

2. **Run Data Cleaning and Transformation**:
   - Use DBT (Data Build Tool) to clean and transform the scraped data:
     ```bash
     dbt run
     ```

3. **Run Object Detection**:
   - Process images using the YOLO model:
     ```bash
     python scripts/object_detection.py
     ```

4. **Start the FastAPI Server**:
   - Launch the FastAPI application to expose the collected data:
     ```bash
     uvicorn main:app --reload
     ```
   - The API will be available at `http://127.0.0.1:8000`.

---

## Key Features

- **Centralized Data Storage**: All data is stored in a data warehouse, enabling efficient querying and analysis.
- **Object Detection**: YOLO is used to extract insights from images, adding a visual dimension to the dataset.
- **API Access**: The FastAPI application provides a user-friendly interface for accessing and querying the data.
- **Scalable Design**: The project is designed to handle large volumes of data and can be extended to include additional data sources or analysis tools.

