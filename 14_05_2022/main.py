import csv
import datetime
import sqlite3
import statistics
from sqlite3 import Error


# Class that represents a sensor value
class SensorValue:
    def __init__(self, temp, timestamp, sensor_id):
        self.temp = temp
        self.timestamp = timestamp
        self.sensor_id = sensor_id

    def __repr__(self):
        return f"SensorValue(temp={self.temp}, timestamp={self.timestamp}, sensor_id={self.sensor_id})"


class SensorValueController:
    def __init__(self, db_file):
        # create database connection
        self.__create_connection(db_file)
        # create table if not exists
        self.__create_table()

    # add a sensor value to the database
    def add_sensor_value(self, sv):
        self.conn.execute("INSERT INTO Temperature (temperature, time, sensorId) VALUES (?, ?, ?)",
                          (sv.temp, sv.timestamp, sv.sensor_id))
        self.conn.commit()  # to force update --> commits transaction

    # removes all values from the database
    def clear_table(self):
        self.conn.execute("DELETE FROM Temperature;")
        self.conn.commit()  # to force update --> commits transaction

    # returns the sensor value with the lowest temperature based on the given filters
    def min(self, sensor_id=None, range_min=None, range_max=None):
        # first get all values
        vals = self.__read_table()
        # if sensor_id is set --> only allow sensor values from the given sensor_id
        if sensor_id is not None:
            # filter the sensor_ids
            vals = list(filter(lambda sv: sv.sensor_id == sensor_id, vals))
        # if at least one range bound is given
        if range_min is not None or range_max is not None:
            # if a minimal timestamp is given use it otherwise use the minimal value
            range_min = range_min if range_min is not None else datetime.datetime.min
            # if a maximal timestamp is given use it otherwise use the maximal value
            range_max = range_max if range_max is not None else datetime.datetime.max
            # filter the sensor values based on the timestamp
            vals = list(filter(lambda sv: range_min <= sv.timestamp <= range_max, vals))

        # if no item is left after filtering return None
        if len(vals) == 0:
            return None
        # use the min function to return the sensor value with the lowest temperature
        return min(vals, key=lambda sv: sv.temp)

    # returns the sensor value with the highest temperature based on the given filters
    def max(self, sensor_id=None, range_min=None, range_max=None):
        # first get all values
        vals = self.__read_table()
        # if sensor_id is set --> only allow sensor values from the given sensor_id
        if sensor_id is not None:
            # filter the sensor_ids
            vals = list(filter(lambda sv: sv.sensor_id == sensor_id, vals))
        # if at least one range bound is given
        if range_min is not None or range_max is not None:
            # if a minimal timestamp is given use it otherwise use the minimal value
            range_min = range_min if range_min is not None else datetime.datetime.min
            # if a maximal timestamp is given use it otherwise use the maximal value
            range_max = range_max if range_max is not None else datetime.datetime.max
            # filter the sensor values based on the timestamp
            vals = list(filter(lambda sv: range_min <= sv.timestamp <= range_max, vals))

        # use the max function to return the sensor value with the highest temperature
        if len(vals) == 0:
            return None
        return max(vals, key=lambda sv: sv.temp)

    def median(self, sensor_id=None):
        # get all values
        vals = self.__read_table()
        # if a sensor id is given filter the values based on the sensor_id
        if sensor_id is not None:
            vals = list(filter(lambda sv: sv.sensor_id == sensor_id, vals))
        # use the statistics.median function to get the median value of all temperatures
        return statistics.median(map(lambda sv: sv.temp, vals))

    # Helper Methods

    # connects to database
    def __create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    # creates database table if not exists
    def __create_table(self):
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS Temperature (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            temperature REAL NOT NULL,
                            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                            sensorId integer 
                        ); """)

    # reads all sensor values from the database and wrap it in SensorValue
    def __read_table(self):
        results = []
        # select all values and fetchall
        for r in self.conn.execute("SELECT * from Temperature").fetchall():
            # deconstruct tuple
            (_, temp, time, sensor_id) = r
            # create SensorValue add to result list
            results.append(SensorValue(temp, datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), sensor_id))
        return results


# function to load the csv and wrap it in SensorValue and add it to the Database
def loadFromCSV(svc, filename="data.csv"):
    # open the database file
    with open(filename) as csvfile:
        # read the csv as dict
        reader = csv.DictReader(csvfile, delimiter=";")
        # for every value create a SensorValue and add to the DataBase
        for row in reader:
            svc.add_sensor_value(
                SensorValue(float(row["temperature"]),
                            datetime.datetime.strptime(row["timestamp"], '%Y-%m-%dT%H:%M:%S'), int(row["sensorid"])))


# Create SensorValueController with sqlite.db as database file
svc = SensorValueController("sqlite.db")
# clear database table
svc.clear_table()
# load data from CSV
loadFromCSV(svc, "data.csv")

# add some more Data
svc.add_sensor_value(SensorValue(13.3, datetime.datetime(2020, 5, 9), 1))
svc.add_sensor_value(SensorValue(14.3, datetime.datetime(2020, 5, 10), 1))
svc.add_sensor_value(SensorValue(15.3, datetime.datetime(2020, 5, 11), 1))
svc.add_sensor_value(SensorValue(13.0, datetime.datetime(2020, 5, 9), 2))
svc.add_sensor_value(SensorValue(14.0, datetime.datetime(2020, 5, 10), 2))
svc.add_sensor_value(SensorValue(15.0, datetime.datetime(2020, 5, 11), 2))

# test min max median for all values
print("Min/Max/Median of all Values\n====")
print(svc.min())
print(svc.max())
print(svc.median())
print("Min/Max/Median for sensor_id=2\n====")
print(svc.min(sensor_id=2))
print(svc.max(sensor_id=2))
print(svc.median(sensor_id=2))
print("Min/Max from 9.5.2020 00:00 to 10.5.2020 00:00\n====")
# test range
print(svc.min(range_min=datetime.datetime(2020, 5, 9), range_max=datetime.datetime(2020, 5, 10)))
print(svc.max(range_min=datetime.datetime(2020, 5, 9), range_max=datetime.datetime(2020, 5, 10)))
