# pylint: disable=all

from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config
import csv
import os


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_data = None
        self.gps_data = None
        self.parking_data = None
        self.reading = False

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        if self.accelerometer_data is None or self.gps_data is None:
            raise ValueError("Data not yet read. Call start_reading first.")
        
        return AggregatedData(
            self.accelerometer_data,
            self.gps_data,
            self.parking_data,
            datetime.now(),
            config.USER_ID,
        )

    def read_csv_file(self, file_path):
        """Читає дані з CSV-файлу та повертає список кортежів."""
        data = []
        try:
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    if self.accelerometer_filename in file_path:
                        data.append(tuple(map(int, row)))
                    elif self.gps_filename or self.parking_filename in file_path:
                        data.append(tuple(map(float, row)))
        except FileNotFoundError:
            print(f"Файл '{file_path}' не знайдено.")
        except Exception as e:
            print(f"Виникла помилка під час читання файлу: {e}")
        return data


    def startReading(self):
        """Починає зчитування файлів"""
        if self.reading:
            print("Already reading.")
            return
        self.reading = True
        self.accelerometer_data = self.read_csv_file(self.accelerometer_filename)
        self.gps_data = self.read_csv_file(self.gps_filename)
        self.parking_data = self.read_csv_file(self.parking_filename)
    
    def stopReading(self):
        """Закінчує зчитування файлів"""
        self.reading = False

