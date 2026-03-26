import requests
import time
import pandas as pd
from datetime import date, datetime, timedelta
from typing import List, Dict
from scrapers.helper import TokenBucket, retry_with_backoff
from api_app.db_manager import DbManager
from bs4 import BeautifulSoup
from config import SOURCES

GREENWAY_DB = SOURCES.get('greenway', {}).get('db_name', 'greenway_db_2026')
from . import Scraper
from api_app.models import GreenWay
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

class GreenWayScraper(Scraper):
    def __init__(self, db_manager=None):
        self.dbManager = db_manager if db_manager else DbManager()
        self.pagination_info = None
        self.data = None
        self.today_date = datetime.now().date().strftime("%Y-%m-%d")
        self.bucket = TokenBucket(rate=1.0, capacity=1.0)
        print("GreenWay Scraper started!")

    def update_url(self, page_number, selected_date):
        base_url = SOURCES.get('greenway', {}).get('base_url')
        return f"{base_url}?page={page_number}&tab_date={selected_date}"

    @retry_with_backoff(max_retries=3, base_delay=2)
    def get_single_page_data(self, url):
        self.bucket.consume()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            raise requests.ConnectionError(f"Status code {r.status_code}")
        if self.pagination_info is None:
            self.pagination_info = r.json()["pagination"]
        self.data = r.json()["data"]
        return self.pagination_info, self.data

    def get_data_from_specific_date(self, selected_date: str):
        all_pages_data = []

        # Fetch first page to initialize pagination info
        first_url = self.update_url(1, selected_date)
        self.get_single_page_data(first_url)
        
        if self.pagination_info["total"] == 0:
            print(f"Total is being zero : {self.pagination_info['total']}")
            return None, {}
            
        all_pages_data += self.data
        last_page_no = int(self.pagination_info["last_page"])
        last_scraped_url = first_url

        # Fetch subsequent pages cleanly safely up to last_page
        for pg_num in range(2, last_page_no + 1):
            daily_price_url = self.update_url(pg_num, selected_date)
            self.get_single_page_data(daily_price_url)

            if len(self.data) > 0:
                all_pages_data += self.data
            else:
                print("Single Page data is being None")
                raise ValueError("Data is none")
            last_scraped_url = daily_price_url

        if len(all_pages_data) != int(self.pagination_info["total"]):
            ## Should add to Logging
            print("Total scraped data isn't equal with info")

        summary_data = {
            "total_rows": self.pagination_info["total"],
            "total_cols": len(self.data[0].keys()),
            "last_scraped_url": daily_price_url,
        }

        return all_pages_data, summary_data

    def scrape_update_daily_data(self):
        try:
            ## Scrape data for specific date
            data, summary = self.get_data_from_specific_date(self.today_date)

            ## summary is being heavy dependent on scraper script
            summary["dataset_name"] = "Green Way Myanmar"
            summary["scraped_date"] = self.today_date
            if data:
                # self.dbManager.insert_batch("greenway_db", data)
                print(f"Insert here! {data}")
                summary["status"] = "success"
            else:
                summary["status"] = "no-data"
                print("Result data from specific date is being None")
            self.dbManager.insert_batch("summary", [summary])
        except ValueError as e:
            print(f"VE : {e}")
            summary["status"] = "fail"

    def get_lastRowData_from_db(self):
        """
        Get the last row (with max id number) and covert to dictionary
        """
        engine = self.dbManager.get_engine()

        # sub_query = select(func.max(GreenWay.id)).scalar_subquery() #  scalar
        sub_query = select(func.max(GreenWay.id)).subquery() ## with normal execute
        # print(sub_query)
        stmt = select(GreenWay).where(GreenWay.id == sub_query)
        with Session(engine) as session:
            # data = session.scalars(stmt).first()
            data = session.execute(stmt).first()

            ## convert to dict
            return data._asdict()['GreenWay'].convert_dict()


    def validate_before_update(self):
        ## get & compare with today scraped data - first row
        pass
