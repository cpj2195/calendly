import time
from pynamodb.exceptions import GetError

from calendly.models import db_helpers 
from calendly.models.users.users_model import Users
from calendly.common.error_handler import DynamoDBError

def create_user(email_id,booked_slots={}):
    """
    Creates an user request

    Parameters
    ----------
    """

    created_ts = int(round(time.time() * 1000))
    user_request = Users(email_id=email_id,booked_slots=booked_slots)
    db_helpers.save_dynamo_object(user_request)



def present_indb(email_id):
    users_result = Users.query(email_id)
    for user in users_result:
        if user.email_id is None:
           return False
        else:
            return True

def get_booked_slots(email_id,my_email):
    try:
        slot_row = Users.get(email_id)
    except GetError:
        raise DynamoDBError("No Such Email Address Found")
    result = {}
    all_slots = slot_row.booked_slots.as_dict()
    if my_email in all_slots:
        result = slot_row.booked_slots.as_dict().get(my_email)
    return result