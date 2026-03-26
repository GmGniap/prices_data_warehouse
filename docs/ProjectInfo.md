# Project Information: Myanmar Commodity & Oil Price Data Scraper

## Current Implementation

### Overview
This project is an ETL (Extract, Transform, Load) pipeline designed to scrape commodity and oil prices in Myanmar from various sources and store them in a database (PostgreSQL/SQLite) for further analysis. A dbt (data build tool) project is also included (but currently ignored per scope) for data transformations.

### Scrapers
The scraping logic is centered in the `scrapers/` directory, using object-oriented Python scripts.
- **Libraries used:** `requests`, `requests-html` (for sites needing JS rendering or heavier HTML parsing), `pandas` (for table extraction and data manipulation), `BeautifulSoup`, etc.
- **Greenway Scraper (`greenway_scraper.py`):** 
  - Hits an undocumented backend API (`https://greenwaymyanmar.com/api/web/market-price`).
  - Iterates through pages until it retrieves all data for the current date.
  - Inserts batch data using SQLAlchemy ORM.
- **Wisarra Scraper (`wisarra_scraper.py`):**
  - Scrapes HTML pages (`https://wisarra.com/en/market-price`) and extracts tables using `pandas.read_html`.
  - Determines page date using XPath via `requests-html`.
- **Citymall & Maxmyanmar:** Other designated scrapers for different commodity/oil prices.
  
### Database Execution
- **`DbManager` (`api_app/db_manager.py`):** Centralizes database connections and execution routines via SQLAlchemy.
- Data is generally inserted using `pandas.DataFrame.to_sql` or direct SQLAlchemy ORM sessions.

### Execution Flow
- `run_all_scrapers.py` acts as the entry point to trigger the daily scraping routines.

---

## Identified Issues & Areas for Improvement

1. **No Rate Limiting:**
   - Scrapers iterate through hundreds of pages (e.g., up to 100 for Wisarra, up to 1000 for GreenWay) rapidly in `while` or `for` loops without any `time.sleep()` or rate limiting. This can lead to IP bans or overwhelm the target servers.
2. **Missing Retry Logic & Error Handling:**
   - Scrapers lack robust backoff strategies (e.g., `tenacity` library or custom retry loops) if a server returns a 500 error or connection timeout.
3. **Hardcoded Iteration Bounds:**
   - Instead of extracting the actual maximum page numbers dynamically, arbitrary high limits are set (e.g., `impossible_pages = 100`).
4. **Lack of User-Agents:**
   - Requests are sent using default library configurations. Adding standard `User-Agent` headers and rotating them minimizes the risk of being blocked.
5. **Automation:**
   - There are references to Airflow (`airflow.sh`, `dags/`) but a simpler, free approach for daily cron jobs on a small scale is **GitHub Actions**.
6. **Logging:**
   - The project relies heavily on `print()` statements. Python's built-in `logging` module should be implemented to record info/errors efficiently.

---

## Next Steps for Improvement (Phase 1)

1. **Add Rate Limiting:** Introduce delays between requests to be polite to target servers.
2. **Enhance API Requests (Best Practices):** Add `User-Agent`, connection timeouts, and basic retry logic.
3. **Automate with GitHub Actions:** Create a `.github/workflows/daily_scraper.yml` to run scripts automatically every day.
