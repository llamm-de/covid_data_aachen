from bs4 import BeautifulSoup
import requests
import re
from dbController import covidDbController
from abc import ABC, abstractmethod

class scraper(ABC):

    def __init__(self, url, db_file):
        self.url = url
        self.db_file = db_file
        self.request = None
        self.soup = None

    def make_request(self):
        # Make request to site
        r = requests.get(self.url)
        if (r.status_code != 200):
            raise requests.ConnectionError("Expected status code 200, but got {}".format(r.status_code))
        else:
            print('Request went through!')
            self.request = r

    def soupify(self):
        # Make beautiful soup object
        self.soup = BeautifulSoup(self.request.text, 'html.parser')

    @abstractmethod
    def scrape(self):
        pass


class covidScraper(scraper):
    def __init__(self, url, db_file):
        self.displayed_date = None
        self.data = None
        super().__init__(url, db_file)


    def scrape(self):
        self.make_request()
        self.soupify()
        self.get_website_date()
        self.get_data_from_htmlTable()
        self.update_database()


    def get_website_date(self):
        # Find a date string in soup object and compare with current date
        month = {'Januar': '01',
                'Februar': '02',
                'März': '03',
                'April': '04',
                'Mai': '05',
                'Juni': '06',
                'Juli': '07',
                'August': '08',
                'September': '09',
                'Oktober': '10',
                'November': '11',
                'Dezember': '12'}

        pattern = r"\d{1,2}[.][ ]?(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)"
        regex = re.compile(pattern)

        for div in self.soup.findAll("div", {"class": "content"}):
            for par in div.findAll('p'):
                match = regex.search(par.text)
                if (match) :
                    match = match.group()
                    splt = match.split('.')
                    if (len(splt[0]) == 1):
                        splt[0] = '0'+splt[0]
                    date_string = splt[0] + '.' + month[splt[1].strip()] + '.2020'
                    self.displayed_date = date_string
                    return
        
        if (self.displayed_date is None):
            raise ValueError('Could not find valid date entry on website!')
        else:
            print('Websites date is: {}'.format(self.displayed_date))


    def get_data_from_htmlTable(self):
        # Scrape data from html table object
        data = {'Aachen':{},
                'Alsdorf':{},
                'Baesweiler':{},
                'Eschweiler':{},
                'Herzogenrath':{},
                'Monschau':{},
                'Roetgen':{},
                'Simmerath':{},
                'Stolberg':{},
                'Würselen':{},
                'noch nicht lokal zugeordnet':{}}
        
        tbl = self.soup.findAll('table')
        for table in tbl:
            rows = table.findAll('tr')
            for row in rows:
                entries = row.findAll('td')
                paragraph = entries[0].find('p')
                if (paragraph is not None):
                    city_name = paragraph.text
                    if (city_name in data):
                        data[city_name] = {'Active': entries[1].find('p').text,
                                        'Total': entries[2].find('p').text}  
        
        self.data = data

    def update_database(self):
        with covidDbController(self.db_file, 'scraper_db') as db:
            db.update_db(self.data, self.displayed_date)
            db.commit()



