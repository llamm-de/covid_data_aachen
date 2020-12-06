import sqlite3
import csv
import json
from geojson import Feature, FeatureCollection
import geopandas as gpd

def export_csv_and_json(locations, cursor):
    # Export case data for all locations
    for location in locations:
        query = "SELECT * FROM {}".format(location)
        data = cursor.execute(query).fetchall()

        # Clean data from null entries
        for id, entry in enumerate(data):
            entry = list(entry)
            for index in range(len(entry)):
                if (entry[index] is None):
                    entry[index] = ''
            data[id] = entry

        # Export to csv files
        filename = '../data/csv/' + location + '.csv'
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Cases', 'Active Cases'])
            writer.writerows(data)

        # Rearrange data for json export
        json_data = {"Date":[],
                     "Cases": [],
                     "Cases Active": []}

        for entry in data:
            json_data['Date'].append(entry[0])
            json_data['Cases'].append(entry[1])
            json_data['Cases Active'].append(entry[2])

        # Export to json files
        filename = '../data/json/' + location + '.json'
        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)

    # Export Deaths data
    query = "SELECT * FROM Deaths"
    data = cursor.execute(query).fetchall()
    filename = '../data/csv/Deaths.csv'
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Age', 'Sex', 'Region'])
        writer.writerows(data)

        # Rearrange data for json export
        json_data = {"Date": [],
                     "Age": [],
                     "Sex": [],
                     "Region": []}

    for entry in data:
        json_data['Date'].append(entry[0])
        json_data['Age'].append(entry[1])
        json_data['Sex'].append(entry[2])
        json_data['Region'].append(entry[3])

    # Export to json files
    filename = '../data/json/Deaths.json'
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


# Export data for particular date using geojson format
def export_geojson(locations, db_cursor):
    shape_data = gpd.read_file('../data/geodata/geodata_ac_region.shp')
    shape_data.at[0, 'GN'] = 'Stolberg'
    
    #shape_data.to_file('test.geojson', driver='GeoJSON')


# Run script
if __name__ == '__main__':
    
    locations = ('Aachen',
                 'Alsdorf',
                 'Baesweiler',
                 'Eschweiler',
                 'Herzogenrath',
                 'Monschau',
                 'Roetgen',
                 'Simmerath',
                 'Stolberg',
                 'Würselen')

    connection = sqlite3.connect('../data/data.db')
    cursor = connection.cursor()

    export_csv_and_json(locations, cursor)

    #export_geojson(locations, cursor)

    print('Successfully exported data from DB!')
