import sqlite3
import csv
import json
from dbController import dbController

# Run script
def export_data():
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

    db = dbController('../data/data.db', 'data_db')
    db.connect()

    # Export case data for all locations
    for location in locations:
        data = db.get_all_from_table(location)

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
    data = db.get_all_from_table('Deaths')
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

    print('Successfully exported data from DB!')
    db.disconnect()
