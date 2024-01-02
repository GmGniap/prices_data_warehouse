from datetime import date, datetime, timedelta
from api_app.db_manager import DbManager
from api_app.models import GreenWay
from scrapers.greenway_scraper import get_data_from_specific_date
from sqlalchemy.orm import Session
from sqlalchemy import select
from tqdm import tqdm


def get_data_and_update_postgres(selected_date, dbManager):
    try:
        ## Scrape data for specific date
        data, summary = get_data_from_specific_date(selected_date)

        ## summary is being heavy dependent on scraper script
        summary["dataset_name"] = "Green Way Myanmar"
        summary["scraped_date"] = selected_date
        if data:
            dbManager.insert_batch("greenway_db", data)
            summary["status"] = "success"
        else:
            summary["status"] = "no-data"
            print("Result data from specific date is being None")
    except ValueError as e:
        print(f"VE : {e}")
        summary["status"] = "fail"
    finally:
        dbManager.insert_batch("summary", [summary])


## Can change below function to test case
def sample_read_data(db):
    engine = db.get_engine()

    stmt = select(GreenWay).where(GreenWay.id == 644740)

    with Session(engine) as session:
        data = session.scalars(stmt).first()
        print(data)
        print(vars(data))


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def scrape_historical_data(dbManager):
    ## Selected start date - 2016-03-16 - to get historical data
    start_date = date(2016, 3, 1)
    today_date = datetime.now().date()
    for daily in tqdm(daterange(start_date, today_date)):
        try:
            get_data_and_update_postgres(daily, dbManager)
            print(f"Finished for {daily}")
        except Exception as e:
            print(f"Error - {e}")
            continue


def main():
    ## Work with Postgres
    dbManager = DbManager()
    # dbManager.reset_tables()  ## Reset tables

    scrape_historical_data(dbManager)
    print("Successfully finished!")


if __name__ == "__main__":
    main()
