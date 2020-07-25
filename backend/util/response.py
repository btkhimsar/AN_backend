import json


def create_resp_dict(status, message):
    resp = {
        'isSuccess': False,
        'message': ''
    }
    if status:
        resp['isSuccess'] = True
    resp['message'] = str(message)
    return resp
