from utils.extract import scrape_data
from utils.transform import clean_data
from utils.load import save_to_csv

def main():
    print("Starting ETL Process...")
    df_raw = scrape_data()
    df_clean = clean_data(df_raw)
    save_to_csv(df_clean)
    print("ETL Process Completed.")

if __name__ == "__main__":
    main()
