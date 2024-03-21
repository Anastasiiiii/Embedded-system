# pylint: disable=all
"""Module providing with an AccelerometerData Schema definition"""

from marshmallow import Schema, fields
from schema.accelerometer_schema import AccelerometerSchema
from schema.gps_schema import GpsSchema


class AggregatedDataSchema(Schema):
    """Class representing an accelerometer data schema"""

    accelerometer = fields.Nested(AccelerometerSchema)
    gps = fields.Nested(GpsSchema)
    timestamp = fields.DateTime("iso")
    user_id = fields.Int()
