from utils.constants import RTN_CODE_SUCCEED, RTN_CODE_FAIL
import json


def response_success_json(param=dict(), request=None, ret_message='Succeeded!'):
    ret = dict()
    ret['ret_code'] = RTN_CODE_SUCCEED
    ret['ret_message'] = ret_message
    if param:
        ret['result'] = param

    response = json.dumps(ret)
    return response


def response_fail_json(ret_code=RTN_CODE_FAIL, ret_message='Failed!'):
    ret = dict()
    ret['ret_code'] = ret_code
    ret['ret_message'] = ret_message
    response = json.dumps(ret)
    return response
