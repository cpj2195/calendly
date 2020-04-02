import time
from calendly.models import db_helpers 
from calendly.models.users.users_model import Users


def store_user_request(email_id):
    """
    Creates an user request

    Parameters
    ----------
    parent_id : String/I
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
