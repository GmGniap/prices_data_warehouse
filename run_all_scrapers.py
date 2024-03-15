# from scrapers.wisarra_scraper import WisarraScraper
# from scrapers.greenway_scraper import GreenWayScraper
from scrapers.helper_funcs.citymall_user_interaction import CityMallUserInteraction
from scrapers.citymall_scraper import CityMallCategoryScraper

# scrapers_dict = {
#     "wisarra": WisarraScraper().scrape_update_daily_data(),
#     "greenway": GreenWayScraper().scrape_update_daily_data(),
# }

# g = GreenWayScraper().get_lastRowData_from_db()

# t = WisarraScraper().scrape_date()
# print(t)


### CityMall Scraping testing for functions

# citymall_ui = CityMallUserInteraction()
# citymall_ui.ask_sub_category_input()

## Testing code for CityMall category scraping
category = CityMallCategoryScraper()
# category.export_all_categories_json('all_categories_March12')
print(category.get_main_category_ids()[2:5])
print("--x--")
print(category.get_sub_ids_under_main('MU_01_FR'))
print("--x--")
print(category.get_sub_ids_under_main('11'))
