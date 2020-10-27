import sqlite3
import csv
import json

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

    connection = sqlite3.connect('data/data.db')
    cursor = connection.cursor()

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
        filename = 'data/csv/' + location + '.csv'
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Cases', 'Active Cases', 'Incidence', 'Death'])
            writer.writerows(data)

        # Rearrange data for json export
        json_data = {"Date":[],
                     "Cases": [],
                     "Cases Active": [],
                     "Incidence": [],
                     "Death": []}

        for entry in data:
            json_data['Date'].append(entry[0])
            json_data['Cases'].append(entry[1])
            json_data['Cases Active'].append(entry[2])
            json_data['Incidence'].append(entry[3])
            json_data['Death'].append(entry[4])

        # Export to json files
        filename = 'data/json/' + location + '.json'
        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)
