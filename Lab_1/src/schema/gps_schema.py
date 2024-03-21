"""Module providing with a Gps Schema definition"""
from marshmallow import Schema, fields


class GpsSchema(Schema):
    """Class representing a gps schema"""

    longitude = fields.Number()
    latitude = fields.Number()
