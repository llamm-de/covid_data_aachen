from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from dbController import dbController

def get_today():
    # Get current date
    today = date.today()
    today = today.strftime("%d.%m.%Y")
    print("Today's date: ", today)
    return today


def make_request(url):
    # Make request to site
    r = requests.get(url)
    if (r.status_code != 200):
        raise requests.ConnectionError("Expected status code 200, but got {}".format(r.status_code))
    else:
        print('Request went through!')
        return r


def get_website_date(soup):
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

    pattern = "\d{1,2}[.][ ]?(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)"
    regex = re.compile(pattern)

    for div in soup.findAll("div", {"class": "content"}):
        for par in div.findAll('p'):
            match = regex.search(par.text)
            if (match) :
                match = match.group()
                splt = match.split('.')
                if (len(splt[0]) == 1):
                    splt[0] = '0'+splt[0]
                date_string = splt[0] + '.' + month[splt[1].strip()] + '.2020'
                return date_string
                


def get_data_from_htmlTable(soup):
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
    
    tbl = soup.findAll('table')
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
    
    return data


def update_database(data, path, date):
    with dbController(path, 'test_db') as db:
        db.update_db(data, date)
        db.commit()

def scraper():
    # Make a request to Aachen.de
    r = make_request('http://aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html')

    # Make beautiful soup object
    soup = BeautifulSoup(r.text, 'html.parser')

    # Check for right date of fetching
    date_string = get_website_date(soup)
    if (date_string is None):
        raise ValueError('Could not find valid date entry on website!')
    else:
        print('Websites date is: {}'.format(date_string))
    
    # Extract data from htmlTable
    data = get_data_from_htmlTable(soup)

    # Update Database
    update_database(data, '../data/data.db', date_string)



