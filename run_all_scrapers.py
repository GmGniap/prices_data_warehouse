# from scrapers.wisarra_scraper import WisarraScraper
# from scrapers.greenway_scraper import GreenWayScraper
from scrapers.helper_funcs.citymall_user_interaction import CityMallUserInteraction
from scrapers.citymall_scraper import CityMallCategoryScraper, CityMallItemsScraper

# scrapers_dict = {
#     "wisarra": WisarraScraper().scrape_update_daily_data(),
#     "greenway": GreenWayScraper().scrape_update_daily_data(),
# }

# g = GreenWayScraper().get_lastRowData_from_db()

# t = WisarraScraper().scrape_date()
# print(t)


### CityMall Scraping testing for functions
## Testing Code for items scraping

# url_test = "https://www.citymall.com.mm/citymall/en/Categories/Grocery/Basic-Grocery/c/11?q=%3Abestselling&page=95"


## UI Testing
citymall_ui = CityMallUserInteraction()
correct_url = citymall_ui.main_interaction()
cm = CityMallItemsScraper(correct_url)

break_count = 10
## Test iterating
print("Start iterating---")
for count, i in enumerate(cm, start=1):
    items = cm.scrape_all_items()
    print(f"No. of items : {len(items)}")
    print(f"Done scraping for count {count}\n")
    if count == break_count:
        break

print("Finished!")
print(items[:10])




## Testing code for CityMall category scraping
# category = CityMallCategoryScraper()
# category.export_all_categories_json('all_categories_March12')

## Test category list
# print(category.get_main_category_ids()[2:5])
# print("--x--")
# print(category.get_sub_ids_under_main('MU_01_FR'))
# print("--x--")
# print(category.get_sub_ids_under_main('11'))
