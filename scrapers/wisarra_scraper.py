import pandas as pd
import ssl
from api_app.db_manager import DbManager
import numpy as np
from requests_html import HTMLSession
from datetime import datetime
from constants import WISARRA_DB

## Need to ignore ssl
ssl._create_default_https_context = ssl._create_unverified_context


class WisarraScraper:
    def __init__(self):
        self.count_page = 0
        self.all_pages_data = []
        print("Scraping Wisarra task started.")
        self.dbManager = DbManager()

    def update_url(self, page_num):
        return f"https://wisarra.com/en/market-price?page={page_num}"

    def get_total_rows(self, df: pd.DataFrame) -> int:
        return df.shape[0]

    def scrape_date(self):
        session = HTMLSession()
        url = self.update_url(1)
        r = session.get(url)
        # find_class = r.html.find("span.container pageContent", first=True)
        if find_class := r.html.xpath("//div[@class='pageContentCon']/div[@class='container pageContent']/*/following::span[1]"):
            page_date = find_class[0].text
            formatted_date = datetime.strptime(page_date, '%B %d, %Y')
            return formatted_date
        print("Not found date")
        return None

    def get_single_data(self, page_num):
        url = self.update_url(page_num)
        data = pd.read_html(url)
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

    def get_all_data_from_single_date(self) -> pd.DataFrame | None:
        try:
            impossible_pages = 100
            for page_num in range(impossible_pages):
                print(f"Scraping Wisarra page: {page_num}")
                self.get_single_data(page_num)
                self.count_page += 1
        except ValueError:
            print(ValueError)
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
                WISARRA_DB , engine, if_exists="append", index=False, method="multi"
            )
            print("Finish insertion.")
            return 200
        else:
            print("Wisarra scraped result return None")
            raise ValueError("Result is none")
