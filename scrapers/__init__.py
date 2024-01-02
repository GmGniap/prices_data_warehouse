from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def scrape_update_daily_data(self):
        pass

    @abstractmethod
    def validate_before_update(self):
        pass
