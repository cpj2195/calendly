import time
from pynamodb.exceptions import GetError

from calendly.models import db_helpers 
from calendly.models.users.users_model import Users
from calendly.common.error_handler import DynamoDBError

def store_user_request(email_id):
    """
    Creates an user request

    Parameters
    ----------
    """

    created_ts = int(round(time.time() * 1000))
    user_request = Users(email_id=email_id)
    db_helpers.save_dynamo_object(user_request)



def present_indb(email_id):
    users_result = Users.query(email_id)
    for user in users_result:
        if user.email_id is None:
           return False
        else:
            return True

def as_dict(user_query):
    
    return {
        'email_id': user_query.email_id,
        'created_ts': user_query.created_ts,
        'booked_slots': user_query.booked_slots.as_dict()
    }


def get_booked_slots(email_id):
    try:
        booked_slots = Users.query(email_id)
    except GetError:
        raise DynamoDBError("No Such Email Address Found")
    for entry in booked_slots:
        result = as_dict(entry).get('booked_slots')
    return result
    