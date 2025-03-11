import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Scrappers:
    def __init__(self, driver_path=None, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
    
    def save_cookies(self, filename, cookies):
        """ Save cookies to a file """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as file:
            pickle.dump(cookies, file)

    def load_cookies(self, filename):
        """ Load cookies from a file """
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        return []

    def check_cookies(self, filename):
        """ Check if cookies file exists """
        return os.path.exists(filename)

    def is_logged_in(self, check_url):
        """ Check if the user is logged in by navigating to a specific page """
        self.driver.get(check_url)
        return self.driver.current_url == check_url

    def login(self, username, password):
        """ Generic login method (to be overridden) """
        raise NotImplementedError("Subclasses must implement login()")

    def scrape_data(self, url, cookies_file, username=None, password=None):
        """ Generic method to handle scraping with cookies """
        self.driver.get(url)
        time.sleep(2)
        if self.check_cookies(cookies_file):
            cookies = self.load_cookies(cookies_file)
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    pass
        else:
            if username and password:
                cookies = self.login(username, password)
                if cookies:
                    self.save_cookies(cookies_file, cookies)
        return self.extract_data(url)

    def extract_data(self, url):
        """ Method to be overridden by subclasses for extracting specific data """
        raise NotImplementedError("Subclasses must implement extract_data()")

