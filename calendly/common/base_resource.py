from builtins import object


class BaseResource(object):

    def __init__(self, query_param=None, path_param=None, body_payload=None,my_email_id=None):
        '''
        This constructor is used to pass parameters and payload of request
        to the resource

        PARAMETERS
        ----------
        query_param: Dict
            This dictionary contains the query params sent
            with the request through the api gateway.

        path_param: Dict
            This dictionary contains path parameters

        body_payload: Dict
            This dictionary contains the body content (payload) sent
            with the request through the api gateway. It is None in case
            of GET request.
        '''
        self.query_param = query_param
        self.path_param = path_param
        self.body_payload = body_payload
        self.my_email_id = my_email_id

    def get(self):
        pass
    
    def post(self):
        pass

    def patch(self):
        pass
    
    def delete(self):
        pass
    
    def put(self):
        pass

    def options(self):
        pass
