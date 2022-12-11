from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import response


# Create your views here.
class KubernetesManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)


class KubernetesNameSpaceManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)


class KubernetesWorkLoadServiceIngressTemplateManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)


class DBManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)


class OrdersManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return response.Response(data="dddd", status=200)
