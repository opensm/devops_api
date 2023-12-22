from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


class RListModelMixin(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(data=serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RRetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(RRetrieveModelMixin, self).retrieve(request, *args, **kwargs)


class RUpdateModelMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().update(request, *args, **kwargs)


class RDestroyModelMixin(mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().destroy(request, *args, **kwargs)


class RCreateModelMixin(mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # return super(mixins.CreateModelMixin, self).create(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)


__all__ = ['RCreateModelMixin', 'RDestroyModelMixin', 'RUpdateModelMixin', 'RListModelMixin', 'RRetrieveModelMixin']
