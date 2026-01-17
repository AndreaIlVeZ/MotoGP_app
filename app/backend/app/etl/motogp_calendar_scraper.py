### script to extract the pdf from motogp. 
### scipr will navgate through the pages, years, class and circuit
### at the bottom of the page there are several pdfs, that need to be dowload
### the pdfs are then stored in a folder structure that mirrors the motogp one
### the pdfs will be then taken by the pdf_tybles

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import logging
import os
import time
import tempfile
import shutil
from urllib.parse import urljoin, urlparse
from pathlib import Path

logger = logging.getLogger(__name__)

class MotoGPCalendarScraper:
    """Scraper to extract calendar of MotoGP website using Selenium"""
    
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
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("ChromeDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            raise
    
    def pdf_extract(self, download_dir: str = None, push_to_supabase: bool = True):
        """Extract PDFs from MotoGP page following the outlined steps
        
        Args:
            download_dir: Directory to store PDFs (if None, uses temporary directory)
            push_to_supabase: Whether to push PDFs to Supabase storage
            
        Returns:
            list: List of downloaded PDF file paths
        """
        try:
            # Create download directory if not provided
            if download_dir is None:
                download_dir = tempfile.mkdtemp(prefix='motogp_pdfs_')
                logger.info(f"Created temporary download directory: {download_dir}")
            else:
                os.makedirs(download_dir, exist_ok=True)
            
            # Configure Chrome to download files to our specified directory
            self._configure_download_directory(download_dir)
            
            downloaded_files = []
            
            # Step 1: Find the elements with xpath //div[contains(@class, "pdf-table__table ")]
            # Should be 3 containers
            xpath_files = '//div[contains(@class, "pdf-table__table ")]'
            
            # Wait for elements to be present
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_files)))
            
            containers = self.driver.find_elements(By.XPATH, xpath_files)
            logger.info(f"Found {len(containers)} PDF table containers")
            
            # Step 2: For each container, find elements by href
            for i, container in enumerate(containers, 1):
                logger.info(f"Processing container {i}/{len(containers)}")
                
                # Find all anchor tags with href attributes (PDF links)
                pdf_links = container.find_elements(By.XPATH, './/a[@href]')
                
                for j, link in enumerate(pdf_links, 1):
                    try:
                        href = link.get_attribute('href')
                        
                        # Check if it's a PDF link
                        if href and href.lower().endswith('.pdf'):
                            logger.info(f"Found PDF link {j}: {href}")
                            
                            # Step 3: Click and download the file
                            pdf_file = self._download_pdf(link, href, download_dir, f"container_{i}_pdf_{j}")
                            if pdf_file:
                                downloaded_files.append(pdf_file)
                                
                    except Exception as e:
                        logger.error(f"Error processing PDF link {j} in container {i}: {e}")
                        continue
            
            logger.info(f"Successfully downloaded {len(downloaded_files)} PDF files")
            
            # Step 4: Push the PDFs to Supabase (if enabled)
            if push_to_supabase and downloaded_files:
                self._push_to_supabase(downloaded_files)
            
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Error in pdf_extract: {e}")
            raise
    
    def _configure_download_directory(self, download_dir: str):
        """Configure Chrome to download files to specified directory"""
        try:
            # Execute Chrome DevTools command to set download behavior
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': download_dir
            })
            logger.info(f"Configured download directory: {download_dir}")
        except Exception as e:
            logger.warning(f"Could not configure download directory: {e}")
    
    def _download_pdf(self, link_element, href: str, download_dir: str, filename_prefix: str) -> str:
        """Download a single PDF file
        
        Args:
            link_element: Selenium WebElement for the link
            href: URL of the PDF
            download_dir: Directory to download to
            filename_prefix: Prefix for the downloaded file
            
        Returns:
            str: Path to downloaded file, or None if failed
        """
        try:
            # Get the original filename from URL
            parsed_url = urlparse(href)
            original_filename = os.path.basename(parsed_url.path)
            
            if not original_filename:
                original_filename = f"{filename_prefix}.pdf"
            
            # Get initial file count in download directory
            initial_files = set(os.listdir(download_dir))
            
            # Click the link to start download
            logger.info(f"Clicking link to download: {original_filename}")
            link_element.click()
            
            # Wait for download to complete
            max_wait_time = 30  # seconds
            wait_interval = 1
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                time.sleep(wait_interval)
                elapsed_time += wait_interval
                
                current_files = set(os.listdir(download_dir))
                new_files = current_files - initial_files
                
                # Check for completed downloads (not .crdownload files)
                completed_files = [f for f in new_files if not f.endswith('.crdownload')]
                
                if completed_files:
                    downloaded_file = completed_files[0]
                    full_path = os.path.join(download_dir, downloaded_file)
                    
                    # Rename file with our prefix if needed
                    if not downloaded_file.startswith(filename_prefix):
                        new_name = f"{filename_prefix}_{downloaded_file}"
                        new_path = os.path.join(download_dir, new_name)
                        shutil.move(full_path, new_path)
                        full_path = new_path
                    
                    logger.info(f"Successfully downloaded: {full_path}")
                    return full_path
            
            logger.warning(f"Download timeout for {original_filename}")
            return None
            
        except Exception as e:
            logger.error(f"Error downloading PDF {href}: {e}")
            return None
    
    def _push_to_supabase(self, file_paths: list):
        """Push downloaded PDFs to Supabase storage
        
        Args:
            file_paths: List of local file paths to upload
        """
        try:
            # Import storage client (assuming it exists)
            from app.storage.storage_client import StorageClient
            
            storage_client = StorageClient()
            storage_client.create_bucket('motogp-pdfs', public=False)
            
            for file_path in file_paths:
                try:
                    filename = os.path.basename(file_path)
                    logger.info(f"Uploading {filename} to Supabase...")
                    
                    # Upload to Supabase bucket (adjust bucket name as needed)
                    storage_client.upload_file(
                        bucket_name='motogp-pdfs',
                        file_path=file_path,
                        object_name=filename
                    )
                    
                    logger.info(f"Successfully uploaded {filename} to Supabase")
                    
                except Exception as e:
                    logger.error(f"Failed to upload {file_path} to Supabase: {e}")
                    
        except ImportError:
            logger.warning("StorageClient not found. Skipping Supabase upload.")
        except Exception as e:
            logger.error(f"Error pushing files to Supabase: {e}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("ChromeDriver closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()