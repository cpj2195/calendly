import datetime
import re
import time
from datetime import date

from calendly.common.error_handler import InvalidInputError
from calendly.models import db_helpers
from calendly.models.users.users_model import Users
from calendly.models.users.users_model_utils import (create_user,
                                                     get_booked_slots,
                                                     present_indb)



def update_slots(email_id,booked_slots,my_email):
    '''
    This function updates the booked_slots column
    in dynamodb when the user tries to book a slot
    with an already present user.
    PARAMETERS
    -----------
    email_id : str
        User with whol you want to book a slot

    booked_slots : dict
        Dict representing already booked slots.

    my_email : str
        Your email id

    '''
    users_obj = Users.get(email_id)
    all_slots = users_obj.booked_slots.as_dict()
    if my_email in all_slots:
        users_obj.booked_slots.as_dict().get(my_email).update(booked_slots)
    else:
        new_calendar_obj = {}
        new_calendar_obj[my_email] = booked_slots
        calender = users_obj.booked_slots.as_dict()
        calender.update(new_calendar_obj)
        users_obj = Users(email_id=email_id,booked_slots=calender)
    db_helpers.save_dynamo_object(users_obj)

def create_slot_json(from_time,to_time,subject=None):
    '''
    This function creates a slot object to be updated
    corresponding to  a date and email in booked_slots
    PARAMETERS
    -----------
    from_time : str
        starting time of the slot

    to_time : str
        Ending time of the event

    subject : str
        Subject of the Meeting
    
    RETURNS
    -------
    object:
       slot response object

    '''
    slot_obj = {}
    slot_obj["from_time"] = from_time
    slot_obj["to_time"] = to_time
    slot_obj["subject"] = subject

    return slot_obj

def date_valid(input_date):
    '''
    This checks if the input date is valid in the following ways:
    1. If the date is possible.
    2. If the date has passed by
    3. If the date follows (dd-mm-yyyy) format.
    It checks if the meeting is for today

    PARAMETERS
    -----------
    input_date : str
        Date of the Meeting
    
    RETURNS
    -------
    bool:
       booking_today
    '''

    booking_today = False
    pattern = re.compile(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}$")
    if not pattern.match(input_date):
      raise InvalidInputError("Date should be in dd-mm-yyyy format")
    try :
        requested_date = datetime.datetime.strptime(input_date, "%d-%m-%Y")
    except ValueError as err:
        raise InvalidInputError("Requested Date is not in the right format")
    todays_date = date.today()
    if(requested_date.day<todays_date.day or requested_date.month<todays_date.month or requested_date.year<todays_date.year):
        raise InvalidInputError("Requested Date has passed by. You cannot book a slot")
    if (requested_date.day==todays_date.day and requested_date.month==todays_date.month and requested_date.year==todays_date.year):
        booking_today = True
    return booking_today

def time_valid(from_time,to_time,booking_today=False):
    '''
    This checks if the input to_time and from_time is valid in the following ways:
    1. If the time follows the 24 hour format.
    2. If the time follows (HH-MM) format.
    3. If the to_time today has already passed away.
    
    PARAMETERS
    -----------
    from_time : str
        starting time of the slot

    to_time : str
        Ending time of the event

    booking_today : bool
        Whether the meeting is set for today

    '''
    timeformat = "%H:%M"
    time_now = datetime.datetime.now()
    pattern = re.compile(r"^[0-9]{2}:[0-9]{2}$")
    if not pattern.match(from_time) or not(pattern.match(to_time)):
      raise InvalidInputError("from_time and to_time should be in HH:MM format")
    try:
        valid_fromtime = datetime.datetime.strptime(from_time, timeformat)
    except ValueError as err:
        raise InvalidInputError("Requested from_time is not in the right format")
    try:
        valid_totime = datetime.datetime.strptime(to_time, timeformat)
    except ValueError as err:
        raise InvalidInputError("Requested to_time is not in the right format")
    if booking_today and (time_now.hour>valid_fromtime.hour):
        raise InvalidInputError("Requested to_time today is not possible")
    elif ((valid_totime.hour<valid_fromtime.hour)):
        raise InvalidInputError("Booking an invalid timeslot or booking is being made accross 2 dates")

def book_slot(my_email,email_id,date,from_time,to_time,subject=None):
    '''
    This function books the slot for the user in the calender of another
    user after doing some prelimanry checks

    
    PARAMETERS
    -----------
    my_email : str
        user requesting the slot

    email_id : str
        slot booked with whom the slot is booked.

    date : str
        Date of the slot

    from_time : str
        starting time of the slot

    to_time : str
        Ending time of the event

    subject : str
        Subject of the slot
        
    '''
    if present_indb(email_id):
        booked_slots = get_booked_slots(email_id,my_email,'book')
        to_book_slot = create_slot_json(from_time,to_time,subject)
        if date not in booked_slots:
            booked_slots[date] = []
        booked_slots[date].append(to_book_slot)
        update_slots(email_id,booked_slots,my_email)
    else :
        raise InvalidInputError("Requested EmailID Is does not exist")
    return True


def free_slot(my_email,email_id,date,from_time,to_time,subject=None):
    '''
    This function frees the slot for the user in the calender of another
    user after doing some prelimanry checks

    
    PARAMETERS
    -----------
    my_email : str
        user requesting the slot

    email_id : str
        slot booked with whom the slot is booked.

    date : str
        Date of the slot

    from_time : str
        starting time of the slot

    to_time : str
        Ending time of the event

    subject : str
        Subject of the slot
        
    '''
    if present_indb(email_id):
        booked_slots = get_booked_slots(email_id,my_email,'free')
        all_events_day = booked_slots.get(date)
        if(not all_events_day):
            raise InvalidInputError("You dont have any booked meetings on that day")
        else:
            to_free_slot = create_slot_json(from_time,to_time,subject)
            all_events_day = list(filter(lambda a: a != to_free_slot, all_events_day))
            users_obj = Users.get(email_id)
            users_obj.booked_slots.as_dict().get(my_email).update({date:all_events_day})
            db_helpers.save_dynamo_object(users_obj)
            return True
    else:
        raise InvalidInputError("You dont have any meeting scheduled with the User")
