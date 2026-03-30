import pandas as pd
import numpy as np


def clean_data(df):
    if df.empty:
        return df

    try:
        df = df.copy()

        # 1. Drop duplicate dulu (lebih aman sebelum cleaning berat)
        df = df.drop_duplicates()

        # 2. Filter invalid rows
        df = df[df['Title'] != 'Unknown Product']
        df = df[df['Price'].notna()]
        df = df[df['Price'] != 'Price Unavailable']

        # =========================
        # 3. CLEAN PRICE
        # =========================
        # Ambil angka (handle $1,200.50 juga)
        df['Price'] = df['Price'].str.replace(r'[^\d.]', '', regex=True)

        # Buang yang kosong
        df = df[df['Price'] != '']

        # Convert ke float → IDR
        df['Price'] = df['Price'].astype(float) * 16000

        # =========================
        # 4. CLEAN RATING
        # =========================
        # Ambil angka rating
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)')

        # Convert ke float
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

        # Drop invalid rating
        df = df.dropna(subset=['Rating'])

        # =========================
        # 5. CLEAN COLORS
        # =========================
        df['Colors'] = df['Colors'].str.extract(r'(\d+)')
        df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')

        # =========================
        # 6. CLEAN SIZE & GENDER
        # =========================
        # Sudah clean dari extract, tapi tetap safe
        df['Size'] = df['Size'].astype(str).str.replace('Size: ', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].astype(str).str.replace('Gender: ', '', regex=False).str.strip()

        # =========================
        # 7. FINAL CLEANING
        # =========================
        df = df.dropna(subset=['Price', 'Colors'])

        # Reset index biar rapi
        df = df.reset_index(drop=True)

        return df

    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame()