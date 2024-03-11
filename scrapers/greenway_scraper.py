import requests
import pandas as pd
from datetime import date, datetime, timedelta
from typing import List, Dict
from api_app.db_manager import DbManager
from . import Scraper
from api_app.models import GreenWay
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

class GreenWayScraper(Scraper):
    def __init__(self):
        self.dbManager = DbManager()
        self.pagination_info = None
        self.data = None
        self.today_date = datetime.now().date().strftime("%Y-%m-%d")
        print("GreenWay Scraper started!")
        
    def update_url(self, page_number, selected_date):
        return f"https://greenwaymyanmar.com/api/web/market-price?page={page_number}&tab_date={selected_date}"

    def get_single_page_data(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise requests.ConnectionError()
        if self.pagination_info is None:
            self.pagination_info = r.json()["pagination"]
        self.data = r.json()["data"]
        return self.pagination_info, self.data

    def get_data_from_specific_date(self, selected_date: str):
        all_pages_data = []
        ## page number should be start from 1 , even though page 1 is the same as page 0
        pg_num = 1
        last_page_no = 1000  ## init impossible number that used to enter while loop

        while pg_num < last_page_no + 1:
            daily_price_url = self.update_url(pg_num, selected_date)
            self.get_single_page_data(daily_price_url)
            if self.pagination_info["total"] == 0:
                print(f"Total is being zero : {self.pagination_info['total']}")
                return None, {}
            last_page_no = int(self.pagination_info["last_page"])
            if len(self.data) > 0:
                all_pages_data += self.data
            else:
                print("Single Page data is being None")
                raise ValueError("Data is none")
            pg_num += 1

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
            
            
            
            # print(vars(data))
    
    def validate_before_update(self):
        ## get & compare with today scraped data - first row
        pass
        
        
