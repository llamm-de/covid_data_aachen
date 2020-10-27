from bs4 import BeautifulSoup
import requests
import re
from datetime import date

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


def match_date_string(soup, today):
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
    
    for heading in soup.findAll('h2'):
        match = re.search(r'\d{2,2}\.\s\w*', heading.text)
        if match:
            match = match.group()
            splt = match.split()
            date_string = splt[0] + month[splt[1]] + '.2020'
            if (date_string == today):
                return True
    return False            


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
    
    table_data = soup.table.findAll('p')
    
    for index, tag in enumerate(table_data):
        if tag.text in data:
            data[tag.text] = {'Active': table_data[index+1].text,
                              'Total': table_data[index+2].text,
                              'Incidence': table_data[index+3].text}
    return data


# Run scraper
if __name__ == '__main__':
    #Get today's date
    today = get_today()
    today = "26.10.2020"

    # Make a request to Aachen.de
    r = make_request('http://aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html')

    # Make beautiful soup object
    soup = BeautifulSoup(r.text, 'html.parser')

    # Check for right date of fetching
    if (match_date_string(soup, today) is not True):
        raise ValueError('Current Date is not equal to date from website!')
    else:
        print('Dates match!')
    
    data = get_data_from_htmlTable(soup)
    print(data)