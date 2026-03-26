from scrapers.wisarra_scraper import WisarraScraper
from scrapers.greenway_scraper import GreenWayScraper
from api_app.db_manager import DbManager
from api_app.models import WatermarkLog
from datetime import datetime

if __name__ == "__main__":
    print("Starting daily scraping tasks...")
    success = True

    try:
        print("Running GreenWay Scraper...")
        g_status = GreenWayScraper().scrape_update_daily_data()
        print(f"GreenWay scraping complete.")
    except Exception as e:
        print(f"Error running GreenWay Scraper: {e}")
        success = False

    try:
        print("Running Wisarra Scraper...")
        w_status = WisarraScraper().scrape_update_daily_data()
        print(f"Wisarra scraping complete. Status: {w_status}")
    except Exception as e:
        print(f"Error running Wisarra Scraper: {e}")
        success = False

    if success:
        print("All scraping tasks finished successfully. Writing watermark...")
        try:
            db = DbManager()
            with db.SessionLocal() as session:
                watermark = WatermarkLog(run_date=datetime.now(), status="SUCCESS")
                session.add(watermark)
                session.commit()
            print("Watermark saved successfully.")
        except Exception as e:
            print(f"Failed to write watermark log: {e}")
    else:
        print("Scraping tasks finished with errors. Watermark not written.")
