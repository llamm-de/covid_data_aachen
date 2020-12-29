import sqlite3
import pandas as pd
import csv
import json

# Database controler
class dbController():

    def __init__(self, path, name):
        self.db_path = path
        self.db_name = name
        self.is_connected = False


    def __enter__(self):
        self.connect()
        return self


    def __exit__(self, type, value, traceback):
        self.disconnect()


    def connect(self):
        if not self.is_connected:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.is_connected = True
        else:
            raise RuntimeError('Database already connected!')


    def disconnect(self):
        if self.is_connected:
            self.connection.close()
            self.is_connected = False
        else:
            raise RuntimeError('Can not disconnect! Database not connected! ')


    def commit(self):
        if self.is_connected:
            self.connection.commit()
        else:
            raise RuntimeError('Can not commit! Database not connected!')


    def get_primary_key(self, table):
        # Find primary key column 
        query = "PRAGMA table_info('{}')".format(table)
        columns = self.cursor.execute(query).fetchall()
        for column in columns:
            if (column[5] == 1):
                return column[1]


    def primary_key_exists(self, table, key):    
        # Check if key exists
        pk_name = self.get_primary_key(table)
        query = r"SELECT EXISTS(SELECT 1 FROM '{}' WHERE {}='{}' COLLATE NOCASE) LIMIT 1".format(table, pk_name, key)
        check = self.cursor.execute(query).fetchone()
        if check[0] == 1:
            return True
        else:
            return False


    def remove_by_key(self, table, key):
        # Remove data entry from table by key
        if self.primary_key_exists(table, key):
            query = r"DELETE FROM {} WHERE Date='{}'".format(table, key)
            self.cursor.execute(query)
        else:
            raise RuntimeError('Can not remove row! Key does not exist!')


    def add_by_key(self, table, key, data_entry):
        # Add data entry into table by key
        query = "INSERT INTO '{}' VALUES ('{}','{}','{}')".format(table, key, data_entry['Total'], data_entry['Active'])
        self.cursor.execute(query)     


    def get_all_from_table(self, table):
        # Get all entries from table
        query = "SELECT * FROM {}".format(table)
        return self.cursor.execute(query).fetchall()


    def get_from_table_by_key(self, table, key):
        # Get entry from table by key
        pass


class covidDbController(dbController):
    
    def __init__(self, path, name):
        super().__init__(path, name) 


    def update_db(self, data, date):
        # Update database with new dataset
        for table in data:
            # Check if primary key exists
            if self.primary_key_exists(table, date):
                raise RuntimeError('Primary key '+ date +' already exists in database!')
            else:
                data_entry = data[table]
                try:
                    self.add_by_key(table, date, data_entry)
                except Exception as e:
                    print("Something went wrong while updating the database!")
                    print(e)
                    exit() 


    def get_location_dataFrame(self, location):
        # Return data for location as PANDAS DataFrame object
        raw_data = self.get_all_from_table(location)
        return pd.DataFrame(raw_data)


    def export_location_data_csv(self, location, path):
        # Export data for location as csv
        filename = path + location + '.csv'
        raw_data = self.get_all_from_table(location)

        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Cases', 'Active Cases'])
            writer.writerows(raw_data)

    
    def export_location_data(self, location, path):
        # Wrapper to export location data fro all supported formats
        self.export_location_data_csv(location, path)
        self.export_location_data_json(location, path)


    def export_location_data_json(self, location, path):
        # Export data for location as json
        filename = path + location + '.json'
        raw_data = self.get_all_from_table(location)
        
        json_data = {"Date":[],
                    "Cases": [],
                    "Cases Active": []}

        for entry in raw_data:
            json_data['Date'].append(entry[0])
            json_data['Cases'].append(entry[1])
            json_data['Cases Active'].append(entry[2])
        
        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)

    
    def export_death_data(self, path):
        # Wrapper to export death data fro all supported formats
        self.export_death_data_csv(path)
        self.export_death_data_json(path)


    def export_death_data_csv(self, path):
        # Export data of death as csv format
        filename = path + 'Deaths.csv'
        raw_data = self.get_all_from_table('Deaths')

        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Age', 'Sex', 'Region'])
            writer.writerows(raw_data)


    def export_death_data_json(self, path):
        # Export data of death as csv format
        filename = path + 'Deaths.json'
        raw_data = self.get_all_from_table('Deaths')
        
        json_data = {"Date": [],
                    "Age": [],
                    "Sex": [],
                    "Region": []}

        for entry in raw_data:
            json_data['Date'].append(entry[0])
            json_data['Age'].append(entry[1])
            json_data['Sex'].append(entry[2])
            json_data['Region'].append(entry[3])

        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)


    def export_all_data_geojson(self, path):
        # Export data for location as geojson
        pass