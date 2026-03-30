import pandas as pd
from sqlalchemy import create_engine

# =========================
# 1. SAVE TO CSV
# =========================
def save_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"[CSV] Data successfully saved to {filename}")
    except Exception as e:
        print(f"[CSV] Error: {e}")


# =========================
# 2. SAVE TO POSTGRESQL
# =========================
def save_to_postgres(df, table_name="products"):
    try:
        DB_URI = "postgresql://postgres:postgres@localhost:5432/dicoding_etl_fpd"
        
        engine = create_engine(DB_URI)

        df.to_sql(
            table_name,
            engine,
            if_exists='replace',  
            index=False
        )

        print("[PostgreSQL] Data successfully saved")

    except Exception as e:
        print(f"[PostgreSQL] Error: {e}")

# =========================
# 3. ORCHESTRATOR
# =========================
def load_all(df):
    if df.empty:
        print("Data kosong, tidak ada yang disimpan.")
        return

    save_to_csv(df)
    save_to_postgres(df)
    # save_to_google_sheets(df)