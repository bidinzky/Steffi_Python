import sqlite3
import requests


class DbValue:
    def __init__(self, date, temp):
        self.date = date
        self.temp = temp

    def __repr__(self):
        return f"{self.date}: {self.temp}"

class DbManager:
    def __init__(self, db_name):
        self.__create_connection(db_name)
        self.__create_table()

    def __create_table(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Temperature (
                               time TIMESTAMP PRIMARY KEY NOT NULL,
                               temperature REAL NOT NULL
                           );""")

    def write_db_value(self, db_value):
        # https://sqlite.org/lang_conflict.html --> see REPLACE
        self.conn.execute("""INSERT or REPLACE INTO Temperature(time, temperature) VALUES (?,?)""", (db_value.date, db_value.temp))
        self.conn.commit()

    def __create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)


def load_weather_data(lat, long):
    hourly = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m").json()["hourly"]
    templist = hourly["temperature_2m"]
    timelist = hourly["time"]
    result = []
    for (time, temp) in zip(timelist, templist):
        result.append(DbValue(time, temp))
    return result


db = DbManager("sqlite.db")
for value in load_weather_data(47.18, 9.79):
    db.write_db_value(value)
