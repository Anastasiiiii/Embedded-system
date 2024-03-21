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
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_data = None
        self.gps_data = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        if self.accelerometer_data is None or self.gps_data is None:
            raise ValueError("Data not yet read. Call start_reading first.")
        
        return AggregatedData(
            self.accelerometer_data,
            self.gps_data,
            datetime.now(),
            config.USER_ID,
        )

    def read_csv_file(self, file_path: str) -> list[list[str]]:
        """Читає дані з CSV-файлу та повертає список рядків."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        
        data = []
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data
    
    def start_reading(self):
        """Починає зчитування файлів"""
        self.accelerometer_data = self.read_csv_file(self.accelerometer_filename)
        self.gps_data = self.read_csv_file(self.gps_filename)
    
    def stop_reading(self):
        """Закінчує зчитування файлів"""
        self.accelerometer_data = None
        self.gps_data = None
    

accelerometer_file_path = 'data/accelerometer.csv'
gps_file_path = 'data/gps.csv'

file_datasource = FileDatasource(accelerometer_filename=accelerometer_file_path, gps_filename=gps_file_path)

file_datasource.start_reading()

aggregated_data = file_datasource.read()

file_datasource.stop_reading()
