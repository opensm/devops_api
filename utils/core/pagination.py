from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from utils import status


# 自定义分页类
class WritePageNumberPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 100
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 1000
    # 获取页码数的
    page_query_param = "page"
    sort_query_param = "sort"

    def get_paginated_response(self, data, message=None, code=status.REQUEST_STATUS_20000_OK):
        """
        :param data:
        :param message:
        :param code:
        :return:
        """
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('message', message),
            ('code', code),
            ('pagesize', self.page.has_other_pages())
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        """
        :param queryset:
        :param request:
        :param view:
        :return:
        """
        params = dict()
        for field in queryset.model._meta.fields:
            for key, value in request.query_params.items():
                if field.name != key:
                    continue
                if type(field).__name__ in ['CharField', 'Textfield']:
                    params["{0}__contains".format(key)] = value
                else:
                    params[key] = value
        queryset = queryset.filter(**params)
        sort_by = request.query_params.get(self.sort_query_param, '+id').strip('+')
        if not hasattr(queryset, sort_by.strip('-')) and sort_by.strip('-') != 'id':
            raise ValueError(
                '不包含字段:{0}'.format(sort_by)
            )
        return super(WritePageNumberPagination, self).paginate_queryset(
            queryset=queryset.order_by(sort_by),
            request=request,
            view=view
        )
