import re


def is_valid_email(email):
    """
    This function checks whether an email address is valid
    or not
    
    PARAMETERS
    ----------
    email: str
        email address
        
    RETURNS
    -------
    boolean
        - whether the email address is valid or not
    """
    return re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").fullmatch(email)
