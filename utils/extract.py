import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_PAGES = 50


def scrape_page(url):
    data_list = []

    response = requests.get(url)

    if response.status_code == 404:
        print(f"{url} -> 404 (skip)")
        return data_list

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('div', class_='collection-card')

    for p in products:
        title_el = p.find('h3', class_='product-title')
        price_el = p.find('span', class_='price')
        detail_elements = p.find_all('p')

        rating = "0"
        colors = "0"
        size = ""
        gender = ""

        for d in detail_elements:
            text = d.get_text(strip=True)

            if "Rating" in text:
                rating = text
            elif "Colors" in text:
                colors = text
            elif "Size" in text:
                size = text.replace("Size:", "").strip()
            elif "Gender" in text:
                gender = text.replace("Gender:", "").strip()

        data = {
            'Title': title_el.get_text(strip=True) if title_el else "Unknown Product",
            'Price': price_el.get_text(strip=True) if price_el else "0",
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data_list.append(data)

    return data_list


def scrape_data():
    all_data = []

    try:
        for i in range(1, MAX_PAGES + 1):
            if i == 1:
                url = BASE_URL
            else:
                url = f"{BASE_URL}page{i}"

            print(f"Scraping halaman {i}...")

            try:
                page_data = scrape_page(url)
                all_data.extend(page_data)
            except Exception as e:
                print(f"Error di halaman {i}: {e}")

            time.sleep(1)

        df = pd.DataFrame(all_data)
        return df

    except Exception as e:
        print(f"Error during extraction: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = scrape_data()
    print(df.head())
    df.to_csv("fashion_data.csv", index=False)