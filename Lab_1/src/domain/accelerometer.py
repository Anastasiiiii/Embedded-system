"""Module with Accelerometer class definition."""
from dataclasses import dataclass


@dataclass
class Accelerometer:
    """Class representing an accelerometer"""

    x: int
    y: int
    z: int
