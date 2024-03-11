from scrapers.greenway_scraper import get_df_from_single_page
from datetime import date, datetime, timedelta

test_date = date(2023, 12, 20).strftime("%Y-%m-%d")

daily_price_url = (
    f"https://greenwaymyanmar.com/api/web/market-price?page=1&tab_date={test_date}"
)


def test_single_page_data():
    test_df = get_df_from_single_page(daily_price_url)
    ## Number of Columns must be 16 cols
    assert test_df.shape[1] == 16
