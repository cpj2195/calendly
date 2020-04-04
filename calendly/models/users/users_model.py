#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from builtins import object

from pynamodb.attributes import (JSONAttribute, MapAttribute, NumberAttribute,
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
        null=False, default=int(round(time.time() * 1000)))
    booked_slots = MapAttribute(default={},null=False)

    def as_dict(self):
        """
        dict representation of Slots related info
        """
        return_Object = self.attribute_values
        return_Object["booked_slots"] = self.booked_slots.as_dict()
