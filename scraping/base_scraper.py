from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from database.db_handler import Database


class BaseScraper(ABC):
    def __init__(self, base_url, db_file):
        self.base_url = base_url
        self.database = Database(db_file)

    def scrape(self):
        for url in self.url_iterator(self.base_url):

            try:
                response = requests.get(url)
                response.raise_for_status()  # Check for any HTTP errors
                html_content = response.text
                # Process the HTML content here
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors
                print("HTTP error occurred:", e)
                continue
            except requests.exceptions.ConnectionError as e:
                # Handle connection errors
                print("A connection error occurred:", e)
                continue
            except requests.exceptions.Timeout as e:
                # Handle timeouts
                print("The request timed out:", e)
                continue
            except requests.exceptions.TooManyRedirects as e:
                # Handle too many redirects
                print("Too many redirects occurred:", e)
                continue
            except requests.exceptions.RequestException as e:
                # Handle any request-related exceptions
                print("An error occurred during the request:", e)
                continue
            except Exception as e:
                # Handle any other exceptions
                print("An error occurred:", e)
                continue

            soup = BeautifulSoup(html_content, 'html.parser')

            if response.status_code == 200 and self.is_valid_page(soup):
                job_listings = self.extract_job_listings(soup)

                filtered_listings = self.filter_job_listings(job_listings)

                for listing in filtered_listings:
                    job_data = self.extract_job_data(listing)
                    if job_data:
                        self.save_to_database(*job_data)

    @abstractmethod
    def url_iterator(self, soup):
        raise NotImplementedError

    @abstractmethod
    def is_valid_page(self, soup):
        raise NotImplementedError

    @abstractmethod
    def is_valid_listing(self, soup):
        raise NotImplementedError

    @abstractmethod
    def extract_job_listings(self, soup):
        raise NotImplementedError

    def filter_job_listings(self, job_listings):
        filtered_listings = []

        for listing in job_listings:
            # Apply your filtering criteria here
            if self.is_valid_listing(listing):
                filtered_listings.append(listing)

        return filtered_listings

    @abstractmethod
    def extract_job_data(self, listing):
        raise NotImplementedError

    def save_to_database(self, job_title, company_name, location, salary, description):
        self.database.insert_job(job_title, company_name, location, salary, description)

    def close_database_connection(self):
        self.database.close_connection()
