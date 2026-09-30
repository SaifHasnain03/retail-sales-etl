from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales.csv"
DB = ROOT / "output" / "sales.db"

def clean_sales(path=INPUT):
    df = pd.read_csv(path, parse_dates=["order_date"])
    df = df.drop_duplicates(subset=["order_id"]).copy()
    numeric = ["quantity", "unit_price", "discount", "revenue"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["order_id", "order_date", "product", "region"])
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    df = df[df["quantity"] > 0]
    return df

def build_database(df, db_path=DB):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        df.to_sql("sales", con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product)")
    return db_path

def run_queries(db_path=DB):
    with sqlite3.connect(db_path) as con:
        monthly = pd.read_sql_query(
            """SELECT strftime('%Y-%m', order_date) AS month,
                      ROUND(SUM(revenue), 2) AS revenue
               FROM sales GROUP BY month ORDER BY month""", con)
        products = pd.read_sql_query(
            """SELECT product, ROUND(SUM(revenue), 2) AS revenue,
                      SUM(quantity) AS units
               FROM sales GROUP BY product ORDER BY revenue DESC""", con)
    return monthly, products

if __name__ == "__main__":
    cleaned = clean_sales()
    build_database(cleaned)
    monthly, products = run_queries()
    print("\nMonthly revenue:")
    print(monthly.to_string(index=False))
    print("\nProduct performance:")
    print(products.to_string(index=False))
