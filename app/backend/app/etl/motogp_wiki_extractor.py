import wikipediaapi

import json 
from datetime import datetime
from app.storage.storage_client import StorageClient

import logging
import os

logger = logging.getLogger(__name__)

### script to export data from wikipedia
### status as of 7/01 - the script works what is mising: 
## * loop over rider pages, circuits pages, seasons pages
## * loop to go over the past years also, with the right naming convention (should be failry simple)
# for now i would say this would be enough from wiki 

### useful info 
# * motogp history generic: https://en.wikipedia.org/wiki/Grand_Prix_motorcycle_racing
# bio for each rider : https://en.wikipedia.org/wiki/Francesco_Bagnaia e.g.
# outline for each rider with list of riders per each year: https://en.wikipedia.org/wiki/2024_MotoGP_World_Championship

# info on the circuits: https://en.wikipedia.org/wiki/List_of_Grand_Prix_motorcycle_circuits
# each circuit page e.g.: https://en.wikipedia.org/wiki/Algarve_International_Circuit

## question how to extract tables with wikipadia api - non lo fa :D 
## per le tabelle fa fatto uno scrapere, ma dato che sono le stesse info provenienti da motogp, non lo fatro


# helper functions 
def extract_sections_structured(sections, level=0):
    info_load = []
    for section in page.sections:
        print(f"Section: {section.title}")
        info_load.append({
            'section_title': section.title,
            'level': section.level,
            'section_text': section.text,
            'subsections': extract_sections_structured(section.sections, level + 1)
        }
        )

    return info_load


def save_wiki_page_as_json(page, page_url, category):
    """Save Wikipedia page as structured JSON"""
    data = {
        "metadata": {
            "page_title": page.title,
            "url": page_url,
            "extraction_date": datetime.now().isoformat(),
            "language": "en",
            "category": category
        },
        "summary": page.summary,
        "full_text": get_full_text(page),
        "sections": extract_sections_structured(page.sections)
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


# add here the push to supabase with client 

def get_full_text(page):
    """
    Combine the summary and all section texts of a Wikipedia page into a single string.

    Args:
        page (wikipediaapi.WikipediaPage): The Wikipedia page object.

    Returns:
        str: The concatenated text of the summary and all sections.
    """
    text = page.summary

    def add_sections(sections):
        for section in sections:
            text_list.append(section.text)
            add_sections(section.sections)

    text_list = [text]
    add_sections(page.sections)
    return " ".join(text_list)


def push_to_supabase(file_paths: list):
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
                    bucket_name='motogp-wiki-data',
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

# Define a user agent string with contact info (as recommended)
user_agent = "MyMotogpAnalyticsApp/1.0 (andreaverba@gmail.com)"

# Create a Wikipedia object with custom headers
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)


motogp_general_page = 'https://en.wikipedia.org/wiki/Grand_Prix_motorcycle_racing'
motogp_general_page_name = motogp_general_page.split('/wiki/')[-1]
### to be done for all the others

example_rider_page = 'https://en.wikipedia.org/wiki/Pedro_Acosta_(motorcyclist)'
example_rider_page_name = example_rider_page.split('/wiki/')[-1]

## championship pages
championship_template = "https://en.wikipedia.org/wiki/2025_MotoGP_World_Championship"
championship_years = [range(2002, 2025)]  # example range from 2002 to 2024
championship_pages = [f"https://en.wikipedia.org/wiki/{year}_MotoGP_World_Championship" for year in championship_years]


# championship_extraction

for i in championship_pages:

    page = wiki.page(i.split('/wiki/')[-1])
    if page.exists():
        print(f"Title: {page.title}\n")
        # stroing and saving section 
        page_json = save_wiki_page_as_json(page, i, category='motogp_championship')
        # push to supabase
        push_to_supabase([page_json])



## continue with riders etc 





