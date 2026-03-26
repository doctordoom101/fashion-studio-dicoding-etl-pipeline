import pandas as pd

def save_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error during loading: {e}")
