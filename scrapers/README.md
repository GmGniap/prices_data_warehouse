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

    - 
```
example.com/petroleum/{publisher_id}/records/{id}
```

```
example.com/{category_id}/{publisher_id}/records/{id}
```