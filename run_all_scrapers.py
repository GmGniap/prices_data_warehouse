# from scrapers.wisarra_scraper import WisarraScraper
# from scrapers.greenway_scraper import GreenWayScraper
from scrapers.helper_funcs.citymall_user_interaction import CityMallUserInteraction
from scrapers.citymall_scraper import CityMallCategoryScraper, CityMallItemsScraper
from scrapers.helper_funcs.export_utils import write_lstOfdicts_into_csv
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


field_names = ['image_url', 'product_name', 'product_url', 'product_price', 'product_sale_price',
                'product_original_price', 'product_seller', 'product_packaging', 'scraped_page_url']

## UI Testing
citymall_ui = CityMallUserInteraction()
correct_url = citymall_ui.main_interaction()
cm = CityMallItemsScraper(correct_url)

break_count = 10
total_items = []
## Test iterating
print("Start iterating---")
for count, i in enumerate(cm, start=1):
    items = cm.scrape_all_items()
    
    ## add one-page items into total
    total_items += items 
    print(f"No. of items : {len(items)}")
    print(f"Done scraping for page count {count}\n")
    if count == break_count:
        break

print("Finished!")
print(len(total_items))
print(total_items[0])
write_lstOfdicts_into_csv(total_items, field_names)




## Testing code for CityMall category scraping
# category = CityMallCategoryScraper()
# category.export_all_categories_json('all_categories_March12')

## Test category list
# print(category.get_main_category_ids()[2:5])
# print("--x--")
# print(category.get_sub_ids_under_main('MU_01_FR'))
# print("--x--")
# print(category.get_sub_ids_under_main('11'))
