from django.utils.deprecation import MiddlewareMixin
from utils.response import DataResponse


class AuthCheckMixin(MiddlewareMixin):

    def process_request(self, request):

        # 做token异常连接
        print("请求打印")
        # if request.method == 'POST':
        #     print(request.POST)
        # print(request.path)
        # if request.path != "/api/auth/user/login" and request.path != "/api/token/":
        #     print(111111111111111111)
        #     try:
        #         auth = request.META.get('HTTP_AUTHORIZATION').split("_")
        #     except AttributeError as e:
        #         return DataResponse(message="登录失败，请检查", code=400)

    def process_response(self, request, response):
        print("返回打印")
        # print(response)
        return response
