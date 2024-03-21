"""Module providing with aggregated data definition"""

from dataclasses import dataclass

from datetime import datetime
from .accelerometer import Accelerometer
from .gps import Gps


@dataclass
class AggregatedData:
    """Class representing aggregated data"""
    accelerometer: Accelerometer
    gps: Gps
    timestamp: datetime
    user_id: int
