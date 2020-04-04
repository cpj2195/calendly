from calendly.common import get_jwt, logger
from calendly.common.error_handler import (InternalServerError,
                                           ResourceNotFoundError,
                                           UnAuthorizedError)
from calendly.resources import resource_constants
from calendly.resources.slots.slot_resource import Slot
from calendly.resources.users.user_resource import User

RESOURCES = {
    'user': User,
    'slots': Slot}


def invoke_resource(resource_name, method_name, params,apitoken):
    '''
    This functions invokes the given method of given resource.
    While invoking, it also passes the parameters given.
    PARAMETERS
    -----------
    resource_name : str
        name of the resource

    method_name : str
        request method name for the resource

    params : str
        parameters to be passed while invoking the resource

    RETURNS
    --------
    dict | str | int:
        result after invoking the  resource

    '''
    resource_class = RESOURCES.get(resource_name)
    if not resource_class:
        error_msg = resource_constants.RESOURCE_NOT_FOUND.format(resource_name)
        logger.log_to_cloudwatch('<ERROR>', error_msg)
        raise ResourceNotFoundError(error_msg)
    resource_object = resource_class()
    super(resource_class, resource_object).__init__(**params)
    try:
        return getattr(resource_object, resource_constants.METHODS[method_name])()
    except Exception as error:
        logger.log_to_cloudwatch('<ERROR>', str(error))
        raise Exception(error)
