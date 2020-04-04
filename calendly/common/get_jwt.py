import jwt

from calendly.common import logger
from calendly.common.error_handler import (AccessDeniedError,
                                           InternalServerError)

secret_key = "1476f4cfa96f20af2ca8cfdf9c5920f54d78f1b835318d729ceec2a72403cc29"

def get_api_token(payload):
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token


def decode_jwt_token(params,apitoken):
    try:
        payload = jwt.decode(apitoken, secret_key, algorithms=['HS256'])
    except Exception as e:
        raise AccessDeniedError(str(e))
    return payload
