from requests_html import HTMLSession

class CityMallScraper:
    def __init__(self, url) -> None:
        self.url = url
        # self.url = "https://www.citymall.com.mm/citymall/en/Categories/Grocery/Basic-Grocery/c/11"
        self.session = HTMLSession()
        
        ## Need to add cookie to set lang = en. If not, default will auto return MM url.
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
             'Cookie' : '_citymallLanguageCookie=en'
             }
        )
        self.data = []
        ## Scraping Initial url for one time
        self.r = self.session.get(self.url)
        print(f"Scrape initial url : {self.url}")
    
    def scrape_next_url(self):
        next_button = self.r.html.find('.page-link.next', first=True)
        if next_link := next_button.links:
            return f"https://www.citymall.com.mm{str(list(next_link)[0])}"
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
                item_dict['product_url'] = check_title.find('a', first=True).attrs['href']
            
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
        return item_dict
    
    ## Scrape all items from one page, return List of Dictionaries
    def scrape_all_items(self):
        items = self.r.html.find('.col-xs-6.col-lg-2.col-md-4.col-sm-4.pt-2.gutter-2.p-1')
        print(f"No. of items : {len(items)}")
        for item in items:
            item_data = self.scrape_item_data_as_dict(item)
            
            ## current scraping url for each item? -> to get page number , category
            
            self.data.append(item_data)
        return self.data
    
    ## Iterate scrape function inside object using iter() and next() magic methods
    def iterate_scrape_func(self, update_url):
        self.r = self.session.get(update_url)
        print(f"Main task : {update_url}")
        
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


url_test = "https://www.citymall.com.mm/citymall/en/Categories/Grocery/Basic-Grocery/c/11?q=%3Abestselling&page=95"
cm = CityMallScraper(url_test)
# next_but = cm.scrape_next_url()
# print(next_but)

## Test iterating
print("Start iterating---")
final_data = []
for count, i in enumerate(cm, start=1):
    items = cm.scrape_all_items()
    final_data += items
    print(len(items))
    print(f"Done scraping for count {count}\n")
print("Finished!")
     