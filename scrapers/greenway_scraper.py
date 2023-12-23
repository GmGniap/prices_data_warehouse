import requests
import pandas as pd
from datetime import date, datetime, timedelta
from typing import List, Dict

# def get_pagination_info(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         raise requests.ConnectionError()
#     pagination_info = r.json()["pagination"]
#     return pagination_info


def get_single_page_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise requests.ConnectionError()
    pagination_info = r.json()["pagination"]
    data = r.json()["data"]
    return pagination_info, data


def get_data_from_specific_date(selected_date: str) -> List:
    data = []
    ## page number should be start from 1 , even though page 1 is the same as page 0
    pg_num = 1
    last_page_no = 1000  ## init impossible number that used to enter while loop

    while pg_num < last_page_no + 1:
        if pg_num == 1:
            # print(f"First Page Num : {pg_num} & Last : {last_page_no}")
            daily_price_url = f"https://greenwaymyanmar.com/api/web/market-price?page={pg_num}&tab_date={selected_date}"
            pagination, single_pg_data = get_single_page_data(daily_price_url)
            if pagination["total"] == 0:
                print(f"Total is being zero : {pagination['total']}")
                return None, {}
            last_page_no = int(pagination["last_page"])
            data += single_pg_data
            pg_num += 1
            continue

        # print(f"After break : Page Num : {pg_num} & Last : {last_page_no}")
        if pagination["total"] > 0:
            daily_price_url = f"https://greenwaymyanmar.com/api/web/market-price?page={pg_num}&tab_date={selected_date}"
            _, single_pg_data = get_single_page_data(daily_price_url)
            if len(single_pg_data) > 0:
                data += single_pg_data
            else:
                print("Single Page data is being None")
                raise ValueError("Data is none")
            pg_num += 1

    if len(data) != int(pagination["total"]):
        ## Should add to Logging
        print("Total scraped data isn't equal with info")

    summary_data = {
        "total_rows": pagination["total"],
        "total_cols": len(single_pg_data[0].keys()),
        "last_scraped_url": daily_price_url,
    }

    return data, summary_data
