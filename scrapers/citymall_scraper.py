from requests_html import HTMLSession
from typing import List, Dict
import json
import re
from copy import deepcopy
from constants import CITYMALL_BASEURL, CITYMALL_CATEGORYURL

en_cache_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Cookie": "_citymallLanguageCookie=en",
}

class CityMallItemsScraper:
    def __init__(self, url) -> None:
        self.url = url
        # self.url = "https://www.citymall.com.mm/citymall/en/Categories/Grocery/Basic-Grocery/c/11"
        self.session = HTMLSession()
        
        ## Need to add cookie to set lang = en. If not, default will auto return MM url.
        self.session.headers.update(
            en_cache_header
        )
        self.all_items_data = []    ## all items data will append into this list
        ## Scraping Initial url for one time
        self.r = self.session.get(self.url)
        ## Show error if not get correct status
        self.r.raise_for_status()
    
    def scrape_next_url(self):
        next_button = self.r.html.find('.page-link.next', first=True)
        if next_link := next_button.links:
            return f"{CITYMALL_BASEURL + str(list(next_link)[0])}"
        print(f"Next link not found : {next_button.attrs['href']}")
        return None
    
    ## Scrape single item data - Need to check some items had special information (like promotion)
    def scrape_item_data_as_dict(self, item) -> dict:
        ## find required data for each item
        item_dict = {
            'image_url' : item.find('.product.img-responsive', first=True).attrs['src']
        }
        if check_title := item.find('.product-title', first=True):
                item_dict['product_name'] = check_title.find('.name', first=True).text
                item_dict['product_url'] = CITYMALL_BASEURL + check_title.find('a', first=True).attrs['href']
            
        if check_price := item.find('.product-price.mt-1', first=True):
            ## if found two span elements , it will be promotional item
            if len(check_price.find('span')) >= 2:  
                item_dict['product_sale_price'] = check_price.find('.product-sale-price', first=True).text
                item_dict['product_original_price'] = check_price.find('.product-original-price', first=True).text
            ## else, it's normal price
            else:
                item_dict['product_price'] = check_price.text
                
        item_dict['product_seller'] = item.find('.product-seller', first=True).find('span', first=True).text
        
        if check_packaging := item.find('.product-packaging', first=True):
            item_dict['product_packaging'] = check_packaging.text
        
        ## current scraping url for each item? -> to get page number , category
        item_dict['scraped_page_url'] = self.url
        return item_dict
    
    ## Scrape all items from one page, return List of Dictionaries
    def scrape_all_items(self):
        items = self.r.html.find('.col-xs-6.col-lg-2.col-md-4.col-sm-4.pt-2.gutter-2.p-1')
        for item in items:
            item_data = self.scrape_item_data_as_dict(item)
            
            ## another question : should I insert into db for each items dict instead of coverting to dataframe at the end
            self.all_items_data.append(item_data)
        return self.all_items_data
    
    ## Iterate scrape function inside object using iter() and next() magic methods
    def iterate_scrape_func(self, update_url):
        self.r = self.session.get(update_url)
        print(f"Current Scraping URL : {update_url}")
        
    ## Only return iterable object (self)
    def __iter__(self):
        return self
    
    ## Next object
    def __next__(self):
        ## get next_button url
        self.next_button = self.scrape_next_url()
        if self.next_button:
            # return self.scrape_new_url(self.next_button)  ## Not working with classmethod
            return self.iterate_scrape_func(self.next_button)
        raise StopIteration
            
    ## ClassMethod to create new scraper project for new url
    @classmethod
    def scrape_new_url(cls, new_url):
        return cls(new_url)
    
    def __str__(self) -> str:
        return f"Current URL : {self.url}"
    
    ## Get all scraping data (List of dictionaries)
    def get_data(self):
        if len(self.data) > 0:
            return self.data


class CityMallCategoryScraper:
    def __init__(self) -> None:
        self.main_url = CITYMALL_CATEGORYURL
        self.main_session = HTMLSession()
        
        self.main_session.headers.update(
            en_cache_header
        )
        self.all_category_lst = []
        self.r = self.main_session.get(self.main_url)
        self.r.raise_for_status()
        
        self.scrape_main_category()
    
    def scrape_main_category(self) -> List[Dict]:
        
        ## Using xpath to select all categories
        all_category_boxes = self.r.html.xpath("//div[contains(@id, 'dep-')]")
        for index, category in enumerate(all_category_boxes):
            ## select category title & url under selected class
            category_dict = {
                'category_title' : category.find(".text-center-xs-sm > p", first=True).text
            }
            # print(f"Scraping Main Category : {category_dict['category_title']}")
            category_dict['category_url'] = CITYMALL_BASEURL + category.find(".text-center-xs-sm > a", first=True).attrs['href']
            if check_id := re.search(r"\/(\w+)$", category_dict['category_url']):
                category_dict['category_id'] = check_id[1]
            else:
                ## one main category doesn't have correct url with digits, set as main-unknown 'MU000'
                # print(f"Main category unknown url : {category_dict['category_url']}")
                category_dict['category_id'] = f'MU_{index:02d}_' + category_dict['category_title'][:2].upper()
            category_dict['sub_categories'] = self.scrape_sub_category(category)
            self.all_category_lst.append(category_dict)
        # print(f"All category length : {len(all_category_lst)}")
        # print(all_category_lst[0])
        # print("---x---")
        return self.all_category_lst

    def scrape_sub_category(self, category_box) -> List[Dict] | List:
        ## find class 'row' > 'col-md-6' that contains sub-category information
        ## Element obj has xpath function to select instead of using 'find()'.
        sub_category_rows = category_box.xpath("//div[@class='row']/div[@class='col-md-6']")
        if len(sub_category_rows) <= 0 : ## to check length of contained sub-category
            # print("Sub-category list is being zero.")
            return []
        sub_category_lst = []
        for sub_index, sub_category in enumerate(sub_category_rows):
            sub_category_dict = {
                'sub_category_title' : sub_category.find('a', first=True).text
                }
            # print(f"Sub-category : {sub_category_dict['sub_category_title']}")
            sub_category_dict['sub_category_url'] = CITYMALL_BASEURL + sub_category.find('a', first=True).attrs['href']
            ## get the last digits from url - some urls can contains words
            if check_sub_id := re.search(r"\/(\w+)$", sub_category_dict['sub_category_url']):
                sub_category_dict['sub_category_id'] = check_sub_id[1]
            else:
                ## Unknown digits - set as sub-unknown 'SU000'
                # print(f"Unknown sub- {sub_category_dict['sub_category_title']} url: {sub_category_dict['sub_category_url']}")
                sub_category_dict['sub_category_id'] = f'SU_{sub_index:03d}_' + sub_category_dict['sub_category_title'][:2].upper()
            sub_category_lst.append(sub_category_dict)
        return sub_category_lst
    
    def get_main_category_ids(self):
        ## Return main category dict without sub_categories list
        all_category_copy = deepcopy(self.all_category_lst) ## If I did shallow copy here, pop action will also affect to the original.
        for category in all_category_copy:
            try:
                category.pop('sub_categories')
            except KeyError as e:
                raise ValueError("sub_categories col isn't found") from e
        return all_category_copy
    
    def get_all_sub_category_ids(self):
        return [{sub_category['sub_category_id'] : sub_category['sub_category_title']} for category in self.all_category_lst for sub_category in category['sub_categories']]
    
    def get_sub_ids_under_main(self, main_category_id: str):
        ## Return list of dictionaries of specific sub_category
        return [
            sub_category
            for category in self.all_category_lst
            for sub_category in category['sub_categories']
            if category['category_id'] == main_category_id
            ]
        
    def export_all_categories_json(self, json_name: str) -> None:
        with open(f'./json_data/{json_name}.json', 'w') as output_file:
            json.dump(self.all_category_lst, output_file)
        
