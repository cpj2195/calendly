from calendly.models.users.users_model_utils import present_indb, get_booked_slots,create_user
from calendly.models.users.users_model import Users
from calendly.common.error_handler import InvalidInputError
from calendly.models import db_helpers
import datetime
import re
from datetime import date
import time

def update_slots(email_id,booked_slots,my_email):
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

def create_slot_json(date,from_time,to_time,subject=None):
    slot_obj = {}
    slot_obj["from_time"] = from_time
    slot_obj["to_time"] = to_time
    slot_obj["subject"] = subject

    return slot_obj

def date_valid(input_date):
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
    timeformat = "%H:%M"
    time_now = datetime.datetime.now()
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

def book_slot(my_email,email_id,date,from_time,to_time,subject=None):
    if present_indb(email_id):
        booked_slots = get_booked_slots(email_id,my_email)
        to_book_slot = create_slot_json(date,from_time,to_time,subject)
        if date not in booked_slots:
            booked_slots[date] = []
        booked_slots[date].append(to_book_slot)
        update_slots(email_id,booked_slots,my_email)
    else :
        raise InvalidInputError("Requested EmailID Is does not exist")
    return True