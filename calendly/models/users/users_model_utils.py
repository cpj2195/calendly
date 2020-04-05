import time

from pynamodb.exceptions import GetError

from calendly.common.error_handler import DynamoDBError,InvalidInputError
from calendly.models import db_helpers
from calendly.models.users.users_model import Users


def create_user(email_id,booked_slots={}):
    '''
    This function creates the user for the first time
    when the user signs up to get apitoken from the server
    and make an entry in the dynamodb.
    PARAMETERS
    -----------
    email_id : str
        email id of the registering user

    booked_slots : dict
        Dict representing already booked slots.
    '''

    created_ts = int(round(time.time() * 1000))
    user_request = Users(email_id=email_id,booked_slots=booked_slots)
    db_helpers.save_dynamo_object(user_request)



def present_indb(email_id):
    '''
    This function checks if a user is already present
    in dynamodb
    PARAMETERS
    -----------
    email_id : str
        user's email_id

    booked_slots : dict
        Dict representing already booked slots.

    RETURNS
    -------
    bool:
       if the user is present or not
    '''
    users_result = Users.query(email_id)
    for user in users_result:
        if user.email_id is None:
           return False
        else:
            return True

def get_booked_slots(email_id,my_email,state='book'):
    '''
    This function gets the booked slots for the user 

    PARAMETERS
    -----------
    email_id : str
        user's email_id

    my_email : str
        api user's email id
    
    state : str
        if the state's = get or free then you 
        cannot view another user's calender if you dont have 
        any meetings with the user.

    RETURNS
    -------
    dict:
       booked slots for the user
    '''
    try:
        slot_row = Users.get(email_id)
    except:
        raise DynamoDBError("No Such Email Address Found")
    result = {}
    all_slots = slot_row.booked_slots.as_dict()
    if my_email in all_slots:
        result = slot_row.booked_slots.as_dict().get(my_email)
    elif(my_email not in all_slots and (state in ['get','free'])):
        raise InvalidInputError("You dont have any slots booked with the mentioned user")
    return result
