# Scrapers to get data from different websites

## API brainstorm
- Available Categories
    - Commodity
        - Rice
    - Petroleum
    - Book

- What do I want to provide?
    - to use in Visualization
        - Filter by categories, by date (from_date / to_date) = date will depend on category, by publishers
        - required fields -> category , publisher, from_date, to_date
        - POST method -> `example.com/object` - object will be dictionary that stored values for required fields

```
example.com/petroleum/{publisher_id}/records/{id}
```

```
example.com/{category_id}/{publisher_id}/records/{id}
```

## Scraping brainstorm
### CityMall Scraping
- Scraping data for every items under around 20 categories. User must be able to use CLI command to select specific category they want to scrape or all data. Result data will be in `.csv` format. Need to think about to store historical data (especially for naming).
- Future updates can be easily match between historical datasets and show the differences.
- Need to package this scraper to be able to share with non-tech people. Use Rye for packaging (or) should I generate `.exe` file using PyInstaller?
- Build CLI app with Click. Which features should be included in CLI?
    - Scrape all categories data - (without concurrency , it will take several mins to scrape. Shouldn't add without concurrency script)
    - Show id options for main categories to scrape.
        - Scrape all data for each category. (Can take longer time for scraping?)
    - Show sub-id for sub-categories to scrape.
        - I should try first to estimate scraping times and think about how to improve. 

#### Scraping 
- Scrape main categories first. Required data : id, category_name, url
- Scrape sub_categories for each main category. Required data : sub_id, parent_id, sub_category_name, url
