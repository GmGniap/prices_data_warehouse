import pandas as pd
import ssl
import requests
import time
import re
from scrapers.helper import TokenBucket, retry_with_backoff
from api_app.db_manager import DbManager
from requests_html import HTMLSession
from datetime import datetime
from config import SOURCES
from typing import Optional

WISARRA_DB = SOURCES.get('wisarra', {}).get('db_name', 'wisarra_db_2026')

## Need to ignore ssl
ssl._create_default_https_context = ssl._create_unverified_context


class WisarraScraper:
    def __init__(self, db_manager=None):
        self.count_page = 0
        self.all_pages_data = []
        self.bucket = TokenBucket(rate=1.0, capacity=1.0)
        print("Scraping Wisarra task started.")
        self.dbManager = db_manager if db_manager else DbManager()

    def update_url(self, page_num):
        base_url = SOURCES.get('wisarra', {}).get('base_url')
        return f"{base_url}?page={page_num}"

    def get_total_rows(self, df: pd.DataFrame) -> int:
        return df.shape[0]

    def scrape_date(self):
        session = HTMLSession()
        url = self.update_url(1)
        r = session.get(url)
        # find_class = r.html.find("span.container pageContent", first=True)
        if find_class := r.html.xpath("//div[@class='pageContentCon']/div[@class='container pageContent']/*/following::span[1]"):
            page_date = find_class[0].text
            ## Example : March 26 , 2026 (or) March 26, 2026.
            match = re.search(r"([A-Za-z]+)\s+(\d{1,2})\s*,\s*(\d{4})", page_date)
            if match:
                clean_date_str = f"{match.group(1)} {match.group(2)}, {match.group(3)}"
                formatted_date = datetime.strptime(clean_date_str, '%B %d, %Y')
                return formatted_date
            else:
                print(f"Date format not matched: {page_date}")
                return None
        print("Not found date")
        return None

    @retry_with_backoff(max_retries=3, base_delay=2)
    def get_single_data(self, page_num):
        url = self.update_url(page_num)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.bucket.consume()
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = pd.read_html(r.text)
        
        if len(data) == 1:
            if self.get_total_rows(data[0]) > 1:
                self.all_pages_data += data
            else:
                raise ValueError(f"Error data : {data[0].iloc[0,0]}")
        elif len(data) > 1:
            print("Multiple table found!")
            raise ValueError("Check multiple table conditions!")
        else:
            raise ValueError("Table not found!")

    def get_all_data_from_single_date(self) -> Optional[pd.DataFrame]:
        try:
            page_num = 1
            while True:
                print(f"Scraping Wisarra page: {page_num}")
                try:
                    self.get_single_data(page_num)
                except ValueError as ve:
                    print(f"Stopping pagination at page {page_num}. Reason: {ve}")
                    break
                self.count_page += 1
                page_num += 1
                time.sleep(1)  ## Add rate limiting delay between pages
        except Exception as e:
            print(f"Other error : {e}")
        finally:
            total_data_len = len(self.all_pages_data)
            print(f"For pages {self.count_page} - {total_data_len}")
            return pd.concat(self.all_pages_data) if total_data_len > 0 else None

    def clean_result_daily_df(self, df: pd.DataFrame) -> pd.DataFrame:
        ## all column names to lower case and strip
        df.columns = df.columns.str.lower().str.strip()
        change_names = {"min": "min_price", "max": "max_price"}

        ## replace change_names
        df.rename(columns=change_names, inplace=True)

        ## convert to integer (or) float type AND replace "-" or blank values with NULL
        df[["min_price", "max_price", "quantity"]] = df[
            ["min_price", "max_price", "quantity"]
        ].apply(pd.to_numeric, errors="coerce")

        ## scrape page date
        df['page_date'] = self.scrape_date()
        # print(df.dtypes)
        return df

    def scrape_update_daily_data(self):
        """
        Scrape daily page data and update to Postgresql tables
        """
        wisarra = self.get_all_data_from_single_date()
        ## Check result is a dataframe , not None
        if isinstance(wisarra, pd.DataFrame):
            wisarra = self.clean_result_daily_df(wisarra)

            ## Update to Postgresql
            engine = self.dbManager.get_engine()
            wisarra.to_sql(
                WISARRA_DB , engine, if_exists="append", index=False, method="multi", chunksize=50
            )
            print("Finish insertion.")
            return 200
        else:
            print("Wisarra scraped result return None")
            raise ValueError("Result is none")
