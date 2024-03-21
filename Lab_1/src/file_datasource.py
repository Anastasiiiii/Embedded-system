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

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        return AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
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
    

accelerometer_file_path = 'data/accelerometer.csv'
gps_file_path = 'data/gps.csv'

file_datasource = FileDatasource(accelerometer_filename=accelerometer_file_path, gps_filename=gps_file_path)

accelerometer_data = file_datasource.read_csv_file(file_datasource.accelerometer_filename)
gps_data = file_datasource.read_csv_file(file_datasource.gps_filename)
