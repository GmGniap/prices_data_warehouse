import sys
import os
import argparse
from datetime import datetime, date
from sqlalchemy import select
from sqlalchemy.orm import Session
from api_app.db_manager import DbManager
from api_app.models import WatermarkLog
from scrapers.wisarra_scraper import WisarraScraper
from scrapers.greenway_scraper import GreenWayScraper
from scrapers.maxmyanmar_scraper import MaxMyanmarScraper

def has_run_today(session: Session, source_name: str) -> bool:
    """Check if there is a SUCCESS watermark for today for the given source."""
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    
    stmt = select(WatermarkLog).where(
        WatermarkLog.source == source_name,
        WatermarkLog.status == "SUCCESS",
        WatermarkLog.run_date >= today_start,
        WatermarkLog.run_date <= today_end
    )
    result = session.execute(stmt).first()
    return result is not None

def log_watermark(session: Session, source_name: str, status: str):
    """Log the execution status of a specific source."""
    watermark = WatermarkLog(source=source_name, run_date=datetime.now(), status=status)
    session.add(watermark)
    session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run daily prices scrapers")
    parser.add_argument('--local', action='store_true', help='Execute on local SQLite database instead of cloud')
    parser.add_argument('--source', type=str, default='all', help='Specify a single source to scrape (e.g., greenway, wisarra, maxmyanmar)')
    args = parser.parse_args()

    print(f"Starting scraping tasks for source: {args.source}...")
    
    try:
        db = DbManager(use_local=args.local)
    except Exception as e:
        print(f"Database Initialization Failed! Check connection: {e}")
        sys.exit(1)
        
    with db.SessionLocal() as session:
        # --- GreenWay Execution ---
        if args.source.lower() in ['all', 'greenway']:
            if has_run_today(session, "greenway"):
                print("GreenWay Scraper already ran successfully today. Skipping to prevent duplicates.")
            else:
                try:
                    print("Running GreenWay Scraper...")
                    GreenWayScraper(db_manager=db).scrape_update_daily_data()
                    print("GreenWay scraping complete.")
                    log_watermark(session, "greenway", "SUCCESS")
                except Exception as e:
                    print(f"Error running GreenWay Scraper: {e}")
                    log_watermark(session, "greenway", "FAILED")

        # --- Wisarra Execution ---
        if args.source.lower() in ['all', 'wisarra']:
            if has_run_today(session, "wisarra"):
                print("Wisarra Scraper already ran successfully today. Skipping to prevent duplicates.")
            else:
                try:
                    print("Running Wisarra Scraper...")
                    WisarraScraper(db_manager=db).scrape_update_daily_data()
                    print("Wisarra scraping complete.")
                    log_watermark(session, "wisarra", "SUCCESS")
                except Exception as e:
                    print(f"Error running Wisarra Scraper: {e}")
                    log_watermark(session, "wisarra", "FAILED")

        # --- MaxMyanmar Execution ---
        if args.source.lower() in ['all', 'max', 'maxmyanmar']:
            if has_run_today(session, "max"):
                print("MaxMyanmar Scraper already ran successfully today. Skipping to prevent duplicates.")
            else:
                try:
                    print("Running MaxMyanmar Scraper...")
                    MaxMyanmarScraper(db_manager=db).scrape_update_daily_data()
                    print("MaxMyanmar scraping complete.")
                    log_watermark(session, "max", "SUCCESS")
                except Exception as e:
                    print(f"Error running MaxMyanmar Scraper: {e}")
                    log_watermark(session, "max", "FAILED")

    print("All configured scraping tasks finished.")
