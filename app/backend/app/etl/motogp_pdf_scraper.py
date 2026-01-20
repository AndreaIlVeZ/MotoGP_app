### script to extract the pdf from motogp. 
### scipr will navgate through the pages, years, class and circuit
### at the bottom of the page there are several pdfs, that need to be dowload
### the pdfs are then stored in a folder structure that mirrors the motogp one
### the pdfs will be then taken by the pdf_tybles


#.---- refactor the navigation part with the expected outome EC 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

import logging
import time
import datetime 
import json

logger = logging.getLogger(__name__)

class MotoGPPDFScraper:
    """Scraper to extract PDFs from MotoGP website using Selenium"""
    
    CALENDAR_URL = "https://www.motogp.com/en/calendar?view=grid"
    
    def __init__(self, headless: bool = True):
        self.driver = None
        self.headless = headless
        self._setup_driver()
    
    def _setup_driver(self):
        """Initialize ChromeDriver with automatic driver management"""
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
    
    def calendar_extract(self, download_dir: str = None, push_to_supabase: bool = True):
        """Extract PDFs from MotoGP page following the outlined steps
        
        Args:
            download_dir: Directory to store PDFs (if None, uses temporary directory)
            push_to_supabase: Whether to push PDFs to Supabase storage
            
        Returns:
            list: List of downloaded PDF file paths
        """
        CALENDAR_URL = "https://www.motogp.com/en/calendar?view=grid"
        try:
                        
            self.driver.get(CALENDAR_URL)
            time.sleep(5)  # attendi che la pagina si carichi completamente

            self.driver.find_element(By.ID, "onetrust-reject-all-handler").click()
            time.sleep(2)  # attendi che il banner scompaia

            # trovare la componente che mi serve
            # xpath '//div[contains(@class, "calendar-listing__grid-view")]'
            calendar = self.driver.find_element(By.XPATH, '//div[contains(@class, "calendar-listing__grid-view")]')
            ## get elements inside the components 

            races = calendar.find_elements(By.CSS_SELECTOR, 'a.calendar-grid-card')
            # Step 2: For each container, find elements by href
            
            races_data = []
            for index, race in enumerate(races, 1):
                try:
                    # Extract attributes from the <a> tag
                    event_id = race.get_attribute("data-event-id")
                    title = race.get_attribute("title")
                    href = race.get_attribute("href")
                    
                    # Extract text from nested elements
                    try:
                        status = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__grid-card-status').text
                    except Exception as e:
                        print(f"⚠️ No status found for race: {e}".format(index))
                        status = None
                    
                    date_range = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__grid-card-date span').text
                    sequence = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__grid-card-event-sequence').text.strip()
                    country = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__grid-card-event-full-name').text
                    event_name = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__grid-card-event-name').text
                    
                    # Extract flag image URL
                    try:
                        flag_url = race.find_element(By.CSS_SELECTOR, '.calendar-grid-card__event-flag').get_attribute('src')
                    except:
                        flag_url = None
                    
                    race_info = {
                        'sequence': int(sequence),
                        'event_id': event_id,
                        'title': title,
                        'country': country,
                        'event_name': event_name,
                        'date_range': date_range,
                        'status': status,
                        'url': href,
                        'flag_url': flag_url
                    }
                    
                    races_data.append(race_info)
                    
                    print(f"{sequence}. {country} - {event_name}")
                    print(f"   Date: {date_range}")
                    print(f"   Status: {status}")
                    print(f"   URL: {href}")
                    print()
                    
                except Exception as e:
                    print(f"❌ Error extracting race {index}: {e}")
                    continue

            self.driver.close()

            print(f"\n✅ Successfully extracted {len(races_data)} races")
            
            # Step 4: Push the PDFs to Supabase as json
            races_df = pd.DataFrame(races_data)

                # Push to Supabase if requested
            if push_to_supabase and races_data:
                self._push_calendar_to_supabase(races_data, races_df)
            
            return races_df
            
        except Exception as e:
            logger.error(f"Error in pdf_extract: {e}")
            raise
    def _push_calendar_to_supabase(self, races_data: list, races_df: pd.DataFrame):
        """Push calendar data to Supabase as JSON (from memory)"""
        try:
            from storage.storage_client import StorageClient
            import io
            
            storage_client = StorageClient()
            storage_client.create_bucket('motogp_data', public=False)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            year = datetime.now().year
            
            # Convert to JSON string
            json_string = json.dumps(races_data, indent=2)
            json_bytes = io.BytesIO(json_string.encode('utf-8'))
            
            # Upload directly from memory
            json_filename = f'calendar_{year}_{timestamp}.json'
            
            # Note: You'll need to add this method to StorageClient
            storage_client.upload_from_memory(
                bucket_name='motogp_data',
                file_content=json_bytes.getvalue(),
                object_name=json_filename,
                folder_path=f'{year}/calendar',
                content_type='application/json'
            )
            
            logger.info(f"✅ Uploaded calendar JSON to Supabase: {json_filename}")
            
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