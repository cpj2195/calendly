import ast

from calendly.common.base_resource import BaseResource
from calendly.common.error_handler import (InvalidInputError,
                                           PayloadValidationError)
from calendly.common.get_jwt import get_api_token
from calendly.models.users.users_model_utils import create_user, present_indb
from calendly.resources import resource_helpers


class User(BaseResource):
       
    def post(self):
        """
        Method to register a user to use calendly API's and return an API token
        to be used subsequent API calls.
        """
        result = {}
        email_id = self.body_payload.get('my_email_id')
        if not email_id:
            raise PayloadValidationError("Invalid key mentioned")
        if not resource_helpers.is_valid_email(email_id):
            raise InvalidInputError("Invalid Email ID")
        if not present_indb(email_id):
            create_user(email_id)
        payload = {"my_email_id":email_id}
        result = {"apiToken":get_api_token(payload)}
        return result
