from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler
from utils.devops_api_log import logger
from rest_framework.response import Response


class ParamErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40004
    message = _('params error.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class DataNotExistException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40001
    message = _('data not found error.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class PermissionDeniedException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40003
    message = _('Permission denied error.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class ServerErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50000
    message = _('Server error.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class ContentErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50003
    message = _('Content error.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class CryptoEncodeException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50000
    message = _('加密异常.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class CryptoDecodeException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50000
    message = _('解密异常.')

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


def rewrite_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    from django.http import Http404
    from rest_framework.exceptions import AuthenticationFailed, ValidationError
    response = exception_handler(exc, context)
    result_data = dict()
    if isinstance(exc, ValueError):
        logger.error("系统内部错误：{}".format(exc))
        result_data['code'] = 50000
        result_data['message'] = "系统内部错误：{}".format(_(str(exc)))
        return Response(status=200, data=result_data)
    if isinstance(exc, Http404):
        logger.error('系统内部错误：{}'.format(exc))
        result_data['code'] = 40004
        result_data['message'] = "系统不存在该资源，请检查！"
        return Response(status=200, data=result_data)
    if isinstance(exc, AuthenticationFailed):
        logger.error('验证错误：{}'.format(exc))
        result_data['code'] = 40001
        result_data['message'] = "登陆失败！"
        return Response(status=200, data=result_data)
    if isinstance(exc, ValidationError):
        logger.error('验证错误：{}'.format(exc))
        result_data['code'] = 50003
        result_data['message'] = "系统内部错误，请联系管理员查看！"
        return Response(status=200, data=result_data)
    if isinstance(exc, AssertionError):
        logger.error('系统内部错误：{}'.format(exc))
        result_data['code'] = 50003
        result_data['message'] = "系统内部错误，请联系管理员查看！"
        # response.status_code = 200
        # response.data = result_data
        return Response(status=200, data=result_data)

    # Now add the HTTP status code to the response.

    if isinstance(exc.detail, dict):
        string_code = exc.detail['code']
        message = exc.detail['detail']
        if 'token_not_valid' == string_code:
            result_data['code'] = 40001
            result_data['message'] = message
        elif 'user_not_found' == string_code:
            result_data['code'] = 40001
            result_data['message'] = message
        elif 'user_inactive' == string_code:
            result_data['code'] = 40001
            result_data['message'] = message
        elif 'password_changed' == string_code:
            result_data['code'] = 40001
            result_data['message'] = message
        elif 'bad_authorization_header' == string_code:
            result_data['code'] = 40003
            result_data['message'] = message
        else:
            result_data['code'] = 50000
            result_data['message'] = message
        if response is not None:
            response.status_code = 200
            response.data = result_data
            return response
    else:
        logger.error('系统内部错误：{}'.format(exc.detail))
        result_data['code'] = 50003
        result_data['message'] = "系统内部错误，请联系管理员查看！"
        response.status_code = 200
        response.data = result_data
        return response


__all__ = [
    'ParamErrorException',
    'DataNotExistException',
    'PermissionDeniedException',
    'ServerErrorException',
    'ContentErrorException',
    'CryptoEncodeException',
    'CryptoDecodeException'
]
