from utils.extract import scrape_data
from utils.transform import clean_data
from utils.load import load_all

def main():
    print("Starting ETL Process...")
    df_raw = scrape_data()
    df_clean = clean_data(df_raw)
    load_all(df_clean)
    print("ETL Process Completed.")

if __name__ == "__main__":
    main()
