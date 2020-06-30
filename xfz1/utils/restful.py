from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    params_errors = 400
    no_auth = 401
    method_errors = 405
    server_errors = 500


def result(code=HttpCode.ok, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def ok():
    return result()


def params_errors(message='', data=None):
    return result(code=HttpCode.params_errors, message=message, data=data)


def no_auth(message='', data=None):
    return result(code=HttpCode.no_auth, message=message, data=data)


def method_errors(message='', data=None):
    return result(code=HttpCode.method_errors, message=message, data=data)


def server_errors(message='', data=None):
    return result(code=HttpCode.server_errors, message=message, data=data)