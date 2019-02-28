from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User
from users.serializers import CreateUserSerializer


def test(request):
    return HttpResponse('test哈哈哈~')


# /username/count
class CheckUsername(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        context = {
            'username': username,
            'count': count
        }
        return Response(context)


class RegiUser(CreateAPIView):
    serializer_class = CreateUserSerializer

