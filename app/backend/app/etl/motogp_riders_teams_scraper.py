# questo ha i combandi per navigare sulle pagine dei risultati. 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

import logging
import time 
import datetime 
import json 

logger = logging.getLogger(__name__)

class MotoGPRidersTeamsScraper:
    """Scraper to get the riders and teams information from MotoGP website"""

    RIDERS_URL = "https://www.motogp.com/en/riders/motogp" 
    TEAMS_URL = "https://www.motogp.com/en/teams/motogp"

    def __init__(self, headless: bool = True):
        self.driver = None
        self.headless = headless
        self._setup_driver()

    def setup_driver(self):
        """Set up automatic ChromeDriver management"""

        try: 
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Automatically download and manage ChromeDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("ChromeDriver initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            raise
    
    def extract_riders_teams(self, download_dir: str = None, push_to_supabase: bool = True  ):
        """Extract riders from the page
        
        args: 


        logic: the teams and riders are in a hierarchy divided by category
            - Motogp , Moto2, Moto3
            - the iteration need to go firs to motogp then the other categories. 
            - the number of riders and teams is different 
        
        """

        try: 
            self.driver.get(self.RIDERS_URL)
            time.sleep(5)

            self.driver.find_element(By.ID, "onetrust-reject-all-handler").click()
            time.sleep(2)

            rider = self.driver.find_element(By.XPATH, '//div[contains(@class, "rider-list__container")]')

            riders = rider.find_elemtns(By.CSS_SELECTOR, 'a.rider-list__rider')

            riders_data = []
            for index, rider_i in enumerate(riders):
                rider_name = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__info-name').text
                rider_team = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__details-country').text
                rider_number = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__background-hashtag').text
                rider_team = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__details-team').text

                riders_data.append({
                    "name": rider_name,
                    "team": rider_team,
                    "number": rider_number
                })
