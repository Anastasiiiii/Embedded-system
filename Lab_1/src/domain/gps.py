"""Module providing with Gps definition"""

from dataclasses import dataclass


@dataclass
class Gps:
    """Class representing Gps"""

    longitude: float
    latitude: float
