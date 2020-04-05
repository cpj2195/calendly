from calendly.common.base_resource import BaseResource
from calendly.common.error_handler import InvalidInputError,PayloadValidationError,InvalidInputError
from calendly.resources import resource_helpers
from calendly.models.users import users_model_utils
from calendly.resources.slots.slot_resource_utils import book_slot,date_valid,time_valid,free_slot
import calendly.resources.resource_constants as cnsts
class Slot(BaseResource):
    
    def get(self):
        """
        Returns information about the booked slots for the user 
        """
        #Case1 : When the user wants to view slots for another person.
        if self.query_param:
            try:
                email_id = self.query_param.get('email_id')
                if not email_id:
                    raise PayloadValidationError("No email_id mentioned")
                result = users_model_utils.get_booked_slots(self.my_email_id,email_id,'get')  
            except ValueError:
                raise InvalidInputError("Invalid Query Paramter mentioned")
            return result
        else:
            raise InvalidInputError("No Query Parameters mentioned")

    def patch(self):
        email_id = self.body_payload.get('email_id')
        date = self.body_payload.get('date')
        from_time = self.body_payload.get('from_time')
        to_time = self.body_payload.get('to_time')
        subject = self.body_payload.get('subject')
        state = self.body_payload.get('state')
        if not date:
            raise PayloadValidationError("Date not mentioned in the payload")
        if not from_time:
            raise PayloadValidationError("From time not mentioned in the payload")
        if not to_time:
            raise PayloadValidationError("To Time not mentioned in the payload")
        if not state or (state not in ['book','free']):
            raise PayloadValidationError("state should be either of book or free")
        booking_today  = date_valid(date)
        time_valid(from_time,to_time,booking_today)
        if not resource_helpers.is_valid_email(email_id):
            raise InvalidInputError(cnsts.INVALID_EMAIL_ID_PROVIDED)
        result = {}
        #Case1 : When the user wants to book a slot with some other person
        if state == 'book' and email_id is not None:
            if book_slot(self.my_email_id,email_id,date,from_time,to_time,subject):
                result["status"] = "booked"

        #Case2 : When the user wants to delete an upcoming slot with another user
        if state=="free" and email_id is not None:
            if free_slot(self.my_email_id,email_id,date,from_time,to_time,subject):
                result["status"] = "Slot Cancelled"
        return result