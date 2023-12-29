from utils.mixins.mixins import *
from rest_framework.generics import GenericAPIView
from django.db import models
from rest_framework.permissions import IsAuthenticated


class RGenericAPIView(GenericAPIView):
    model = None
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        assert self.model, "model is required!"
        assert not isinstance(self.model, models.Model), "model type is not Model!"
        # _fields = self.model._fields
        return self.model.objects.all()

    def get_paginated_response(self, data, **kwargs):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, **kwargs)


class CreateAPIView(
    RCreateModelMixin,
    RGenericAPIView
):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(
    RListModelMixin,
    RGenericAPIView
):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(
    RRetrieveModelMixin,
    RGenericAPIView
):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(
    RDestroyModelMixin,
    RGenericAPIView
):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(
    RUpdateModelMixin,
    RGenericAPIView
):
    """
    Concrete view for updating a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(
    RListModelMixin,
    RCreateModelMixin,
    RGenericAPIView
):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(
    RRetrieveModelMixin,
    RUpdateModelMixin,
    RGenericAPIView
):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(
    RRetrieveModelMixin,
    RDestroyModelMixin,
    RGenericAPIView
):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(
    RRetrieveModelMixin,
    RUpdateModelMixin,
    RDestroyModelMixin,
    RGenericAPIView
):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


__all__ = [
    'CreateAPIView', 'ListCreateAPIView', 'ListAPIView',
    'RetrieveUpdateAPIView', 'RetrieveUpdateDestroyAPIView',
    'RetrieveDestroyAPIView', 'UpdateAPIView', 'RGenericAPIView', 'RetrieveAPIView'
]
