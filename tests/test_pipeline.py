import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline import clean_sales

def test_clean_sales_has_expected_columns():
    df = clean_sales()
    assert {"order_id", "order_date", "product", "revenue"}.issubset(df.columns)

def test_revenue_is_non_negative():
    df = clean_sales()
    assert (df["revenue"] >= 0).all()

def test_order_ids_are_unique():
    df = clean_sales()
    assert df["order_id"].is_unique
