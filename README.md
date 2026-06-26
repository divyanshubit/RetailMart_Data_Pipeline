# RetailMart_Data_Pipeline

## Project Overview
This project simulates a real-world retail data engineering pipeline for RetailMart Pvt. Ltd. The goal of the project is to ingest, clean, transform, and load retail sales data for business reporting and analysis.

## Technologies Used
- Python
- Pandas
- NumPy
- SQLite
- Git & GitHub

## Dataset Files
- sales.csv
- products.csv
- stores.csv

## Project Workflow
1. Data Ingestion
   - Loaded CSV files using Pandas.

2. Data Cleaning
   - Removed duplicate records.
   - Filled missing values in quantity with 0.
   - Removed rows with missing amount values.
   - Converted data types appropriately.

3. Data Transformation
   - Merged sales, products, and stores datasets.
   - Calculated total revenue for each transaction.
   - Generated city-wise revenue analysis.

4. Data Loading
   - Loaded the cleaned dataset into SQLite database.

5. Reporting & Insights
   - Top 3 selling products.
   - Revenue per store per day.
   - Top selling city and product.

## Key Features
- Automated ETL pipeline using `run_pipeline()`
- Error handling using try-except blocks
- SQL-based reporting
- Business insights generation

## How to Run
```bash
python pipeline.py