import ast
from calendly.common.base_resource import BaseResource
from calendly.common.error_handler import InvalidInputError
from calendly.common.get_jwt import get_api_token
from calendly.resources import resource_helpers
class User(BaseResource):
    
    def get(self):
        """
        Returns information about the current user

        To be Done
        """

        return "Hello World"
    
    def post(self):
        """
        pass
        """
        if self.query_param:
            try:
                email_id = self.query_param.get('email_id')
                print(email_id)
                if not resource_helpers.is_valid_email(email_id):
                    raise InvalidInputError("Invalid Email ID")
            except ValueError:
                raise InvalidInputError("Invalid Query Parameter Mentioned")
            payload = {"email_id":email_id}
            result = {"apiToken":get_api_token(payload)}
        else:
            raise InvalidInputError("No Query Parameter Mentioned")
        return result