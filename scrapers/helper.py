import time
import requests
from functools import wraps
from datetime import timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def compare_two_dictionaries(first_dict : dict, second_dict : dict) -> bool:
    for key in first_dict.keys():
        if first_dict[key] != second_dict[key]:
            return False
    return True

class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def consume(self, tokens: float = 1.0):
        while True:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return
            
            # Not enough tokens, calculate how long to wait
            deficit = tokens - self.tokens
            wait_time = deficit / self.rate
            time.sleep(wait_time)

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.HTTPError, requests.exceptions.Timeout) as e:
                    if attempt == max_retries - 1:
                        print(f"Failed after {max_retries} attempts: {e}")
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
        return wrapper
    return decorator
