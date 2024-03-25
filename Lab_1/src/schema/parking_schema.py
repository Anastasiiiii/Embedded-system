# pylint: disable=all
"""Module providing with an Parking Schema definition"""

from schema.gps_schema import GpsSchema
from marshmallow import Schema, fields

class ParkingSchema(Schema):
    """Class representing a parking schema"""
    empty_count = fields.Number()
    gps = fields.Nested(GpsSchema)