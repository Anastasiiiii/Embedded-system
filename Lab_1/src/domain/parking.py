# pylint: disable=all
"""Module providing with Parking definition"""
from domain.gps import Gps

class Parking:
    """Class representing Parking"""
    empty_count: int
    gps: Gps