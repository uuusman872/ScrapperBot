from selenium.webdriver.common.by import By
from scrapper import Scrappers
import random
import time


class FacebookScrapper(Scrappers):
    def __init__(self, driver_path=None, headless=False):
        super().__init__(driver_path, headless)
    
    def login(self, username, password):
        try:
            self.driver.get("https://www.facebook.com/")
            email = self.driver.find_element(By.XPATH, "//input[@type='text']")
            passwd = self.driver.find_element(By.XPATH, "//input[@type='password']")
            email.send_keys(username)
            passwd.send_keys(password)
            submit = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Log in')]")
            submit.click()
        except Exception as e:
            print("unable to complete login process with error ", e)

        try:
            save_div = self.driver.find_element(By.XPATH, "//div[@role='button' and .//*[contains(text(), 'Save')]]")
            save_div.click()
        except Exception as e:
            print("unable to perform click action on save button with error ", e)

        if self.is_logged_in("https://www.facebook.com/settings"):
            return self.driver.get_cookies()
        return None
    
    def extract_data(self, profile_url, max_limit=100, pause_time_range=(2, 5), scroll_amount=500):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        profile_url += "/friends"
        self.driver.get(profile_url)
        result = []
        while True:
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(*pause_time_range))
            friends_div = self.driver.find_elements(By.XPATH, '//div[@class="x78zum5 x1q0g3np x1a02dak x1qughib"]/div')
            for friend in friends_div:
                data = {}
                try:
                    username = friend.find_element(By.XPATH, './/a[@tabindex="0"]/span')
                    data["name"] = username.text
                    data["profile_link"] = friend.find_element(By.XPATH, ".//a").get_attribute("href")
                    data["username"] = data["profile_link"].split("/")[-1]
                except Exception:
                    pass
                if data:
                    result.append(data)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return result

if __name__ == "__main__":
    fb_scrapper = FacebookScrapper()
    result = fb_scrapper.scrape_data(url="https://www.facebook.com/nina.visser.3", username="03326044222", password="blacklotus", cookies_file="scrappers/cookies/facebook.pkl")
