from scraper import scraper
from export_data import export_data
from scraper import covidScraper

if __name__ == "__main__":

    URL = 'http://aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html'

    # Run the scraper
    scraper = covidScraper(URL, '../data/data.db')
    scraper.scrape()

    # Export data from db
    export_data()