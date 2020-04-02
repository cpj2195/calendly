#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ast
from calendly.common.logger import log_to_cloudwatch
from calendly.events.resource_list import invoke_resource


def respond(err, res=None):
    '''
    To prepare the response payload with the  headers required for the
    cross origin access of the lambda functions through the api gateway.

    PARAMETERS
    -------------
    err : Exception
        errors
    res : Dict
        response to be sent
    '''
    body = {}
    if err:
        try:
            body["message"] = err.args[0].message
            body["type"] = err.args[0].error_type
        except:
            body["message"] = str(err)
            body["type"] = "None"
    else:
        body = res
    response_obj = {
        'statusCode': err.args[0].status_code if err else '200',
        'body': json.dumps(body)
    }
    return response_obj


def main(event, context):
    """
    This is the main handler function which is executed first when the
    lambda function is invoked.
    This functions is invoked by aws lambda by passing the following arguments:
    1) event
    2) context
    For more information refer :
    http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

    This functions inturn call all the working functions and returns the
    result fetched from these functions.

    PARAMETERS
    ------------
    event : dict
        Object that contains all the parameters passed while invoking the
        lambda function
    context : LambdaContext
        object that contains the runtime information about the lambda function.

    RETURNS
    ------------
    response : dict
        response to the caller
    """
    resource_name = resource(event)
    method_name = http_method(event)
    params = parameters(event)
    try:
        result = invoke_resource(resource_name, method_name, params)
        error_obj = None
        response_obj = get_response_obj(error_obj, result)

    except Exception as error_obj:
        log_to_cloudwatch("ERROR:", error_obj)
        result = None
        response_obj = get_response_obj(error_obj, result)
    return response_obj


def get_response_obj(error_obj, result):
    '''
    This function returns the response object in both the cases when the request
    is successfull or not.


    PARAMETERS
    ----------
    error_obj : Python Object
        Object which is None in if the request is successfull or 
    result : dict | str | int:
        result after invoking the  resource

    RETURNS
    -------
    object:
       Response object

    '''
    response_obj = respond(error_obj, result)
    return response_obj


def resource(event):
    '''
    This function returns the resource name on which the client requested.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function

    RETURNS
    -------
    str:
        Name of the resource

    '''
    RESOURCE = 'resource'
    return event[RESOURCE][1:]


def http_method(event):
    '''
    This function returns the HTTP Method name with which the client requested
    the resource.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function

    RETURNS
    -------
    str:
        Name of the HTTP Method

    '''
    HTTP_METHOD = "httpMethod"

    return event[HTTP_METHOD]


def parameters(event):
    '''
    This function returns the data that has been sent with request from
    the client.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function

    RETURNS
    -------
    Dict:
        Dict that contains the query_params and the body data. Example value
        could be :
            {
                'query_param':{'id':1999}
                'body_payload':{'state':'state','value':'completed'}
            }

    '''
    QUERY_PARAM_STRING = 'queryStringParameters'
    PATH_PARAMETERS = 'pathParameters'
    body_payload = json.loads(event.get('body')) if (
        event.get('body')) else None
    if body_payload and body_payload.get("payload") and type(
            body_payload.get("payload")) is not dict:
        body_payload['payload'] = ast.literal_eval(body_payload['payload'])
    params_dict = {
        'query_param': event.get(QUERY_PARAM_STRING),
        'path_param': event.get(PATH_PARAMETERS),
        'body_payload': body_payload,
    }
    return params_dict
