# Retail Sales ETL Pipeline

A complete Python data engineering project that takes raw retail sales data, cleans and validates it, loads it into SQLite, and produces SQL based business summaries.

## What this demonstrates

- Python data ingestion and transformation
- Data cleaning and validation
- SQLite data warehousing
- SQL aggregation and indexing
- Reproducible project structure
- Automated tests with pytest

## Pipeline

`sales.csv` -> cleaning and validation -> SQLite database -> SQL analytics

## Results

The pipeline produces monthly revenue and product performance summaries in the console and stores the cleaned dataset in `output/sales.db`.

## Run locally

```bash
pip install -r requirements.txt
python src/pipeline.py
pytest
```

## Tech stack

Python, Pandas, SQLite, SQL, Pytest

## Dataset

The dataset is synthetic and generated specifically for this project, so it contains no personal or commercial data.
