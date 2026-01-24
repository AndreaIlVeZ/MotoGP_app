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
import pandas as pd

logger = logging.getLogger(__name__)

class MotoGPRidersTeamsScraper:
    """Scraper to get the riders and teams information from MotoGP website"""

    RIDERS_URL = "https://www.motogp.com/en/riders" 
    TEAMS_URL = "https://www.motogp.com/en/teams"

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
    
    def extract_riders(self, push_to_supabase: bool = True  ):
        """Extract riders from the page
        
        logic: the teams and riders are in a hierarchy divided by category
            - Motogp , Moto2, Moto3
            - the iteration need to go firs to motogp then the other categories. 
            - the number of riders and teams is different 
        
        """
        competition_categories = ['motogp', 'moto2', 'moto3']
        riders_data = []

        for category in competition_categories:

            EXTRACT_URL = self.RIDERS_URL + '/'+ category

            try: 
                self.driver.get(EXTRACT_URL)
                time.sleep(5)

                try:
                    # Wait up to 5 seconds for the cookie banner to appear
                    cookie_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
                    )
                    cookie_button.click()
                    logger.info("Cookie banner dismissed")
                    time.sleep(1)
                except Exception as e:
                    # Cookie banner didn't appear or was already dismissed
                    logger.info("No cookie banner to dismiss")

                rider = self.driver.find_element(By.XPATH, '//div[contains(@class, "rider-list__container")]')

                riders = rider.find_elements(By.CSS_SELECTOR, 'a.rider-list__rider')

                riders_load = []
                for index, rider_i in enumerate(riders):
                    rider_name = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__info-name').text
                    rider_country = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__details-country').text
                    rider_number = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__background-hashtag').text
                    rider_team = rider_i.find_element(By.CSS_SELECTOR, 'div.rider-list__details-team').text
                    rider_stat_page = rider_i.get_attribute('href')

                    riders_load.append({
                        "sequence_id": index,
                        "category": category,
                        "name": rider_name,
                        "country": rider_country,
                        "team": rider_team,
                        "number": rider_number,
                        "page_ref": rider_stat_page
                    })
                logger.info(f"Extracted {len(riders_data)} riders from MotoGP page")
            
                riders_data.extend(riders_load)

            except Exception as e:
                logger.error(f"Error extracting riders: {e}")
                raise

        self.driver.quit()

        riders_df = pd.DataFrame(riders_data)
        if push_to_supabase and riders_data:
            self._push_riders_to_supabase(riders_df)

        return riders_df
    

    def extract_teams(self, push_to_supabase: bool = True):
        """Extract teams from the page
        
        logic: the teams are in a hierarchy divided by category
            - Motogp , Moto2, Moto3
            - the iteration need to go firs to motogp then the other categories. 
            - the number of riders and teams is different 
        
        """
        competition_categories = ['motogp', 'moto2', 'moto3']
        teams_data = []

        for category in competition_categories:

            EXTRACT_URL = self.TEAMS_URL + '/'+ category

            try: 
                self.driver.get(EXTRACT_URL)
                time.sleep(5)

                try:
                    # Wait up to 5 seconds for the cookie banner to appear
                    cookie_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
                    )
                    cookie_button.click()
                    logger.info("Cookie banner dismissed")
                    time.sleep(1)
                except Exception as e:
                    # Cookie banner didn't appear or was already dismissed
                    logger.info("No cookie banner to dismiss")

                teams_list = self.driver.find_element(By.XPATH, '//div[contains(@class, "-list__container")]')

                teams = teams_list.find_elements(By.CSS_SELECTOR, 'a.teams-list__team')

                teams_load = []
                for index, team in enumerate(teams):
                    team_name = team.find_element(By.CSS_SELECTOR, 'div.teams-list__info-name').text
                    team_riders = team.find_element(By.CSS_SELECTOR, 'div.teams-list__info-container').text
                    team_stat_page = team.get_attribute('href')

                    teams_load.append({
                        "sequence_id": index,
                        "category": category,
                        "name": team_name,
                        "riders": team_riders,
                        "page_ref": team_stat_page
                    })
                logger.info(f"Extracted {len(teams_load)} riders from MotoGP page")
            
                teams_data.extend(teams_load)

            except Exception as e:
                logger.error(f"Error extracting riders: {e}")
                raise

        self.driver.quit()

        teams_df = pd.DataFrame(teams_data)
        if push_to_supabase and teams_data:
            self._push_riders_to_supabase(teams_df)

        return teams_df
    


    def _push_teams_to_supabase(self, teams_data: list):
        """Push teams data to Supabase as JSON (from memory)"""
        try:
            from storage.storage_client import StorageClient
            import io
            
            storage_client = StorageClient()
            storage_client.create_bucket('motogp_data', public=False)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            year = datetime.now().year
            
            # Convert to JSON string
            json_string = json.dumps(teams_data, indent=2)
            json_bytes = io.BytesIO(json_string.encode('utf-8'))
            
            # Upload directly from memory
            json_filename = f'calendar_{year}_{timestamp}.json'
            
            # Note: You'll need to add this method to StorageClient
            storage_client.upload_from_memory(
                bucket_name='motogp_data',
                file_content=json_bytes.getvalue(),
                object_name=json_filename,
                folder_path=f'{year}/teams',
                content_type='application/json'
            )
            
            logger.info(f"✅ Uploaded teams JSON to Supabase: {json_filename}")
            
        except Exception as e:
            logger.error(f"Error pushing calendar to Supabase: {e}")
            raise

    def _push_riders_to_supabase(self, riders_data: list):
        """Push riders data to Supabase as JSON (from memory)"""
        try:
            from storage.storage_client import StorageClient
            import io
            
            storage_client = StorageClient()
            storage_client.create_bucket('motogp_data', public=False)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            year = datetime.now().year
            
            # Convert to JSON string
            json_string = json.dumps(riders_data, indent=2)
            json_bytes = io.BytesIO(json_string.encode('utf-8'))
            
            # Upload directly from memory
            json_filename = f'calendar_{year}_{timestamp}.json'
            
            # Note: You'll need to add this method to StorageClient
            storage_client.upload_from_memory(
                bucket_name='motogp_data',
                file_content=json_bytes.getvalue(),
                object_name=json_filename,
                folder_path=f'{year}/riders',
                content_type='application/json'
            )
            
            logger.info(f"✅ Uploaded riders JSON to Supabase: {json_filename}")
            
        except Exception as e:
            logger.error(f"Error pushing calendar to Supabase: {e}")
            raise

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("ChromeDriver closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()