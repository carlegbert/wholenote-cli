from .auth import construct_bearer_header, refresh_request
from .exceptions import FailedRequestException


def send_request(access_token, method, url, data=None, refresh_count=0):
    """ Send request and return data on success. Return None and display
    error message on failure.
    """
    header = construct_bearer_header(access_token)

    if data:
        res = method(url, headers=header, json=data)
    else:
        res = method(url, headers=header)

    if res.status_code == 200:
        return res.json()
    elif refresh_count > 3:
        raise FailedRequestException(res.status_code, 'Error authenticating \
                                     token. You may need to log in again.')
    elif res.status_code == 422:
        access_token = refresh_request()
        refresh_count += 1
        return send_request(access_token, method, url, data, refresh_count)
    else:
        raise FailedRequestException(res.status_code, res.json()['msg'])
