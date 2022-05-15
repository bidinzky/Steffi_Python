import datetime
import sqlite3
import statistics
from sqlite3 import Error
from dataclasses import dataclass
from typing import List


@dataclass
class SensorValue:
    temp: float
    time: datetime.datetime
    sensor_id: int


class SensorValueController:
    def __init__(self, db_file):
        self.conn = SensorValueController.__create_connection(db_file)
        self.__create_table()

    def add_sensor_value(self, sv: SensorValue):
        self.conn.execute("INSERT INTO Temperature (temperature, time, sensorId) VALUES (?, ?, ?)",
                          (sv.temp, sv.time, sv.sensor_id))
        self.conn.commit()  # to force update --> commits transaction

    def clear_table(self):
        self.conn.execute("DELETE FROM Temperature;")
        self.conn.commit()  # to force update --> commits transaction

    def min(self, sensor_id: int = None, range_min: datetime.datetime = None, range_max: datetime.datetime = None):
        return self.__min_max(is_min=True, sensor_id=sensor_id, range_min=range_min, range_max=range_max)

    def max(self, sensor_id: int = None, range_min: datetime.datetime = None, range_max: datetime.datetime = None):
        return self.__min_max(is_min=False, sensor_id=sensor_id, range_min=range_min, range_max=range_max)

    def median(self, sensor_id: int = None):
        vals = list(self.__read_table())
        if sensor_id is not None:
            vals = self.__filter_sensor_id(vals, sensor_id)

        return statistics.median(map(lambda sv: sv.temp, vals))

    # Helper Methods

    @staticmethod
    def __create_connection(db_file):
        try:
            return sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def __create_table(self):
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS Temperature (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            temperature REAL NOT NULL,
                            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                            sensorId integer 
                        ); """)

    def __read_table(self):
        for r in self.conn.execute("SELECT * from Temperature").fetchall():
            (_, temp, time, sensor_id) = r
            yield SensorValue(temp, datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), sensor_id)

    def __min_max(self, is_min=True, sensor_id: int = None, range_min: datetime.datetime = None,
                  range_max: datetime.datetime = None):
        vals = list(self.__read_table())
        if sensor_id is not None:
            vals = self.__filter_sensor_id(vals, sensor_id)

        if range_min is not None or range_max is not None:
            range_min = range_min if range_min is not None else datetime.datetime.min
            range_max = range_max if range_max is not None else datetime.datetime.max
            vals = self.__filter_range(vals, range_min, range_max)

        fn = min if is_min else max
        return fn(vals, key=lambda sv: sv.temp)

    @staticmethod
    def __filter_sensor_id(vals: List[SensorValue], i: int) -> List[SensorValue]:
        return list(filter(lambda sv: sv.sensor_id == i, vals))

    @staticmethod
    def __filter_range(vals: List[SensorValue], r_min: datetime.datetime, r_max: datetime.datetime):
        return list(filter(lambda sv: r_min <= sv.time <= r_max, vals))


svc = SensorValueController("sqlite.db")
svc.clear_table()
svc.add_sensor_value(SensorValue(13.3, datetime.datetime(2020, 5, 9), 1))
svc.add_sensor_value(SensorValue(14.3, datetime.datetime(2020, 5, 10), 1))
svc.add_sensor_value(SensorValue(15.3, datetime.datetime(2020, 5, 11), 1))
svc.add_sensor_value(SensorValue(13.0, datetime.datetime(2020, 5, 9), 2))
svc.add_sensor_value(SensorValue(14.0, datetime.datetime(2020, 5, 10), 2))
svc.add_sensor_value(SensorValue(15.0, datetime.datetime(2020, 5, 11), 2))
# test all
print("====")
print(svc.min())
print(svc.max())
print(svc.median())
print("====")
# test sensor_id
print(svc.min(sensor_id=2))
print(svc.max(sensor_id=2))
print(svc.median(sensor_id=2))
print("====")
# test range
print(svc.min(range_min=datetime.datetime(2020, 5, 9), range_max=datetime.datetime(2020, 5, 10)))
print(svc.max(range_min=datetime.datetime(2020, 5, 9), range_max=datetime.datetime(2020, 5, 10)))
