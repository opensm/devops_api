import logging

from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer


class APIResponse(Response):
    """
    自定义Response返回数据：
    return APIResponse(data={"name":'11111111'},request_id='11111111')
    return APIResponse(data={"name":'11111111'})
    return APIResponse(errcode='101', errmsg='错误',data={"name":'11111111'}, header={})
    """

    def __init__(self, code=0, message=None, data=None, status=None, headers=None, **kwargs):
        dic = {'code': code, 'message': message}
        if data:
            dic = {'code': code, 'message': message, 'data': data}
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)


class DataResponse(JsonResponse):

    def __init__(self, code, message, status=200, data=None, **kwargs):
        if data or data == []:
            data_dict = {"data": data, 'message': message, "code": code}
        else:
            data_dict = {'message': message, "code": code}
        if kwargs:
            for key, val in kwargs.items():
                data_dict[key] = val
        super().__init__(data=data_dict, status=status)


class YSQResponse(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not data:
            result = {
                "message": "操作成功！",
                "code": 20000
            }
            logging.warning("没有收到返回数据：{}".format(result))
            renderer_context['response'].status_code = 200

            return super().render(
                data=result,
                accepted_media_type=accepted_media_type,
                renderer_context=renderer_context
            )
        if not isinstance(data, dict):
            logging.warning("收到得数据不是dict：{}".format(data))
            renderer_context['response'].status_code = 200

            return super().render(
                data=data,
                accepted_media_type=accepted_media_type,
                renderer_context=renderer_context
            )
        data_keys = data.keys()
        if 'message' in data_keys and 'code' in data_keys:
            result = data
        else:
            result = {
                "message": "操作成功！",
                "code": 20000,
                "data": data
            }
        return super().render(result, accepted_media_type, renderer_context)


__all__ = ['DataResponse', 'APIResponse', 'YSQResponse']
