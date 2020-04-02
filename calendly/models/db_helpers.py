from pynamodb.exceptions import PutError
from calendly.common.error_handler import DynamoDBError


def save_dynamo_object(pynamo_object):
    """
    Saves a Pynamo Object to DynamoDB.

    Parameters
    ----------
    pynamo_object: Pynamo Object
        A pynamo model object to save in the database
    """
    try:
        pynamo_object.save()
    except PutError as err:
        raise DynamoDBError("Not able to insert the Entry in DB")
