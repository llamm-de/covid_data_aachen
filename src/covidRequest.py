import requests
import pandas as pd
from datetime import datetime

class covidRequest():
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.success = False
        self.request = None
        

    def make_request(self):
        request = requests.get(self.api_url)
        if (request.status_code != 200):
            raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))
        else:
            print('Request went through!')
            self.request = request
            self.success = True


class covidDataAcRequest(covidRequest):
    
    def __init__(self, api_url):
        self.data = {'Aachen':[],
                     'Alsdorf':[],
                     'Baesweiler':[],
                     'Eschweiler':[],
                     'Herzogenrath':[],
                     'Monschau':[],
                     'Roetgen':[],
                     'Simmerath':[],
                     'Stolberg':[],
                     'Würselen':[],
                     'Städteregion':[],
                     'noch nicht lokal zugeordnet':[]}
        self.data_extracted = False
        super().__init__(api_url)

    
    def extract_data(self):
        # Get raw data from request
        raw_data = self.request.json()
        raw_data = raw_data['features']
        
        # Clean up data set
        for item in raw_data:
            single_set = item['attributes']
            location = single_set['Kommune']
            del single_set['Creator']
            del single_set['Kommune']
            single_set['Meldedatum'] = datetime.fromtimestamp(single_set['Meldedatum']//1000)
            self.data[location].append(single_set)

        self.data_extracted = True


    def get_location_dataframe(self, location):
        return pd.DataFrame(self.data[location])
        

    def get_all_dataframe(self):
        df = []
        for location in self.data:
            df.append(self.get_location_dataframe(location))
        return df