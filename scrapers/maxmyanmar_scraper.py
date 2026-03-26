import pandas as pd
import requests
import json
from datetime import datetime
from config import SOURCES
from scrapers.helper import TokenBucket, retry_with_backoff
from api_app.db_manager import DbManager

MAX_DB = SOURCES.get('max', {}).get('db_name', 'max_db_2026')

class MaxMyanmarScraper:
    def __init__(self, db_manager=None):
        self.dbManager = db_manager if db_manager else DbManager()
        self.bucket = TokenBucket(rate=1.0, capacity=1.0)
        print("MaxMyanmar Scraper started!")
        
    @retry_with_backoff(max_retries=3, base_delay=2)
    def fetch_data(self, url, payload, headers):
        self.bucket.consume(1)
        response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def scrape_update_daily_data(self):
        t = datetime.today().date()
        base_url = SOURCES.get('max', {}).get('base_url', 'https://app.maxenergy.com.mm/maxapi/webapi/Price/GetPriceList')
        
        payload = json.dumps({
            "apikey": "R2wwQjRBdTFIbUY4OUFXRTZpbWZuYzhtVkxXd3NBYXdqWXI0Unh6YUNFTGdM",
            "fromdate": f"{t} 12:00:00 AM",
            "todate": f"{t} 11:00:00 PM"
        })
        headers = {
            'content-type': 'application/json',
            'Cookie': '.AspNetCore.Session=CfDJ8B0ta%2BbvQ0RLgbpaxcGdndgbCvK8BQSCNXPXosRd%2BsHPqTu3gVO7Z%2FTID1K2qyncCqw53HbvlUzTyAVYixfNnnZgMYT2siiOV1L0gzKGdYEe%2BYMldYcAlsYqWyohDi4g8t3Y49A%2FKGPoF4BHk1179zRtsuFT6ujfa6Zg8J%2Fxtzeg'
        }

        print(f"Scraping MaxMyanmar for date: {t}")
        data_json = self.fetch_data(base_url, payload, headers)
        raw_data = data_json.get('data', [])
        
        if not raw_data:
            print("No data received from MaxMyanmar API today.")
            return

        raw_df = pd.json_normalize(raw_data)
        clean_df = raw_df[raw_df['price'] != 0.0].reset_index(drop=True)
        
        # Add scraping date securely
        clean_df['scraping_date'] = pd.to_datetime('today').normalize()

        print(f"Data Extracted: {clean_df.shape}")

        engine = self.dbManager.get_engine()
        clean_df.to_sql(MAX_DB, engine, if_exists="append", index=False)
        print("MaxMyanmar scraping and insertion forcefully completed.")