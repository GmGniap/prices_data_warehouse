# from scrapers.wisarra_scraper import WisarraScraper
from scrapers.greenway_scraper import GreenWayScraper

# scrapers_dict = {
#     "wisarra": WisarraScraper().scrape_update_daily_data(),
#     "greenway": GreenWayScraper().scrape_update_daily_data(),
# }

g = GreenWayScraper().get_lastRowData_from_db()

# t = WisarraScraper().scrape_date()
# print(t)
