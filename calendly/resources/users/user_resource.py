import ast

from calendly.common.base_resource import BaseResource
from calendly.common.error_handler import (InvalidInputError,
                                           PayloadValidationError,MethodNotDefined)
from calendly.common.get_jwt import get_api_token
from calendly.models.users.users_model_utils import create_user, present_indb
from calendly.resources import resource_helpers
import calendly.resources.resource_constants as cnsts

class User(BaseResource):
       
    def get(self):
        """
        Not allowed for this resource.
        """
        raise MethodNotDefined()

    def post(self):
        """
        Method to register a user to use calendly API's and return an API token
        to be used subsequent API calls.
        """
        result = {}
        email_id = self.body_payload.get(cnsts.MY_EMAIL_ID)
        if not email_id:
            raise PayloadValidationError("Invalid key mentioned")
        if not resource_helpers.is_valid_email(email_id):
            raise InvalidInputError(cnsts.INVALID_EMAIL_ID_PROVIDED)
        if not present_indb(email_id):
            create_user(email_id)
        payload = {cnsts.MY_EMAIL_ID:email_id}
        result = {cnsts.APITOKEN:get_api_token(payload)}
        return result

    def patch(self):
        """
        Not allowed for this resource.
        """
        raise MethodNotDefined()
    
    def put(self):
        """
        Not allowed for this resource.
        """
        raise MethodNotDefined()