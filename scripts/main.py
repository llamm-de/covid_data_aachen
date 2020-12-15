from scraper import covidScraper
from dbController import covidDbController
import pandas as pd

if __name__ == "__main__":

    URL = 'http://aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html'
    DB_FILE = '../data/data.db'
    LOCATIONS = ('Aachen',
                 'Alsdorf',
                 'Baesweiler',
                 'Eschweiler',
                 'Herzogenrath',
                 'Monschau',
                 'Roetgen',
                 'Simmerath',
                 'Stolberg',
                 'Würselen')

    # Run the scraper
    scraper = covidScraper(URL)
    scraper.scrape()

    # Set up database connection and update database
    db = covidDbController(DB_FILE, 'database')
    db.connect()
    db.update_db(scraper.data, scraper.displayed_date)

    # Export data from db 
    for location in LOCATIONS:
        db.export_location_data_csv(location, '../data/csv/')
        db.export_location_data_json(location, '../data/json/')
    
    db.export_death_data_csv('../data/csv/')
    db.export_death_data_json('../data/json/')