from calendly.common.base_resource import BaseResource
from calendly.common.error_handler import InvalidInputError,PayloadValidationError
from calendly.resources import resource_helpers
from calendly.models.users import users_model_utils


class Slot(BaseResource):
    
    def get(self):
        """
        Returns information about the booked slots for the user 
        """
        #Case1 : When the user request booked slots for another user for the coming week.
        if self.query_param:
            try:
                email_id = self.query_param.get('email_id')
            except ValueError:
                raise InvalidInputError("Invalid Query Paramter mentioned")
            result = users_model_utils.get_booked_slots(email_id)  
            return result
        #Case2 : When the user wants to view his own booked slots for the coming week
        else:
            pass

    def patch(self):
        email_id = self.body_payload.get('engine_data')
        date = self.body_payload.get('parent_type')
        from_time = self.body_payload.get('parent_id')
        to_time = self.body_payload.get('engine_type')
        subject = self.body_payload.get('subject')
        if not date:
            raise error_handler.PayloadValidationError("Date not mentioned in the payload")
        if not from_time:
            raise error_handler.PayloadValidationError("From time not mentioned in the payload")
        if not to_time:
            raise error_handler.PayloadValidationError("To Time not mentioned in the payload")
        #Case1 : When the user wants to book a slot with some other person
        


        #case2 : When the user wants to book a slot a personal slot


        #case3 : When the user wants to delete an upcoming slot with another user


        #case4 : When the user wants to free his own personal slot