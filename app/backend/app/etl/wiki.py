import wikipediaapi


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

## insert a for loop con tutte le parti che voglio estrarre, questo va fatto e ahggiornato in parte
### alcuni file cambiano sempre altri no

### agglomerare in una funzione unica 
page = wiki.page(example_rider_page_name)

# Check if the page exists and display a clean summary
if page.exists():
    print(f"Title: {page.title}\n")
    print("Summary:")
    print(page.summary if len(page.summary) < 1000 else page.summary[:1000] + "...")
else:
    print(f"The page {example_rider_page_name} does not exist on Wikipedia.")


## continuare qui per estrapolare il testo e sezioni
""
def print_sections(sections, level=0):
    """
    Recursively prints the titles of Wikipedia page sections with indentation.

    Args:
        sections (list): List of wikipediaapi.WikipediaPageSection objects.
        level (int, optional): Current indentation level. Defaults to 0.
    """
    for section in sections:
        print(f"{'  ' * level}{section.title}")
        print_sections(section.sections, level + 1)

print_sections(page.sections)

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


full_text = get_full_text(page).lower()
print(full_text[:2000])  # Print the first 2000 characters of the full text

