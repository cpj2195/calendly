#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builtins import object
import os
import time

from pynamodb.attributes import (NumberAttribute,MapAttribute,
                                 UnicodeAttribute)

from calendly.models import db_constants as credentials
from calendly.models.pynamo_base_model import PynamoBaseModel


class Users(PynamoBaseModel):
    """
    Dynamo DB model for the Users table.
    """

    class Meta(object):
        table_name = credentials.DYNAMO_USERS_TABLE
        region = credentials.DYNAMO_REGION

    email_id = UnicodeAttribute(hash_key=True,null=False)
    created_ts = NumberAttribute(
        null=False, default=int(round(time.time() * 1000)),range_key=True)
    booked_slots = MapAttribute(default={},null=False)
    