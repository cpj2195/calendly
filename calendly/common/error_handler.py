#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calendly.common import error_codes as cnts

class BaseExceptionError(Exception):
    status_code = 500
    message = cnts.BASE_ERROR
    error_type = cnts.err_BaseExceptionError_code

    def __init__(self, message=None, error_type=None,
                 status_code=None, payload=None):
        Exception.__init__(self)
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['messages'] = self.message
        return rv

    def __str__(self):
        return self.message


class InvalidInputError(BaseExceptionError):
    message = cnts.INVALID_INPUT
    error_type = cnts.err_InvalidInputError_code
    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class PayloadValidationError(BaseExceptionError):
    message = cnts.INVALID_PAYLOAD_PARAMETER
    error_type = cnts.err_PayloadValidationError_code
    
    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class EmptyPayloadError(BaseExceptionError):
    message = cnts.EMPTY_PAYLOAD
    error_type = cnts.err_EmptyPayloadError_code

    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class ResourceNotFoundError(BaseExceptionError):
    message = cnts.RESOURCE_NOT_FOUND.format('Resource')
    error_type = cnts.err_ResourceNotFoundError_code
    status_code = 404

    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type, self.__class__.status_code)


class NotFoundError(BaseExceptionError):
    message = cnts.NOT_FOUND
    error_type = cnts.err_NotFoundError_code

    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class DynamoDBError(BaseExceptionError):
    message = cnts.DYNAMO_DB_OP_ERR
    error_type = cnts.err_DynamoDBError_code

    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class MethodNotDefined(BaseExceptionError):
    message = cnts.METHOD_NOT_FOUND
    status_code = 405
    error_type = cnts.err_MethodNotDefined_code

    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type = error_type
        super(self.__class__, self).__init__(message, error_type)

class InternalServerError(BaseExceptionError):
    message = cnts.INTERNAL_SERVER_ERROR
    status_code = 500
    def __init__(self, message=None, error_type=None):
        if message:
            self.message = message
        if error_type:
            self.error_type =  error_type
        super(self.__class__, self).__init__(message, error_type)
