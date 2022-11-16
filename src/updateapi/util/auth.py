import datetime

from updateapi.util.auth import Token

def check_authentication(token: str) -> bool:
    """
     Checks authentication of static token:
     1) Token must exist in database
     2) Token must not be expired

     :param: token: str: a token secret to check

     :return: bool: whether token is valid
    """
    tokens = Tokens.objects(secret=token)
    if len(tokens) == 0:
        return False
    assert len(tokens) == 1, "Duplicating tokens found"
    token = tokens[0]
    if int(datetime.datetime.now.timestamp()) > token.expire:
        return False
    return True
