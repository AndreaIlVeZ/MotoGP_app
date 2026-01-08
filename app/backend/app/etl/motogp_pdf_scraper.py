### script to extract the pdf from motogp. 
### scipr will navgate through the pages, years, class and circuit
### at the bottom of the page there are several pdfs, that need to be dowload
### the pdfs are then stored in a folder structure that mirrors the motogp one
### the pdfs will be then taken by the pdf_tybles

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import logging

logger = logging.getLogger(__name__)

class MotoGPPDFScraper:
    """Scraper to extract PDFs from MotoGP website using Selenium"""
    
    MAIN_PAGE = 'https://www.motogp.com/en'
    
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
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("ChromeDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            raise
    
    def pdf_extrac(self):

        # find the elements with xpath //div[contains(@class, "pdf-table__table ")]
        ## should be 3 
        xpath_files = '//div[contains(@class, "pdf-table__table ")]'
        containers = self.driver.find_elements(by='xpath', value = xpath_files)
        for container in containers:
            # find elements by href
        # then for each href in the list click and download the file. the driver has to 
        # locate the filed from download and store them in a temporary directory
        # then push the pdf to supabase 

        return 

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("ChromeDriver closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()