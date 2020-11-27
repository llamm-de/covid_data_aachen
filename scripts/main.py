from scraper import scraper
from export_data import export_data

if __name__ == "__main__":
    # Run the scraper
    scraper()

    # Export data from db
    export_data()