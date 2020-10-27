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

    connection = sqlite3.connect('data/test.db')
    cursor = connection.cursor()

    for location in locations:
        query = "SELECT * FROM {}".format(location)
        data = cursor.execute(query).fetchall()
        
        # Export to csv files
        filename = 'data/csv/' + location + '.csv'
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Cases', 'Active Cases', 'Incidence', 'Death'])
            writer.writerows(data)

        # Export to json files
        
