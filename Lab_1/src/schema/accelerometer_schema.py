"""Module providing with an Accelerometer Schema definition"""
from marshmallow import Schema, fields


class AccelerometerSchema(Schema):
    """Class representing an accelerometer schema"""
    x = fields.Int()
    y = fields.Int()
    z = fields.Int()
