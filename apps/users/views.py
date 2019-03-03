from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User, Area
from users.serializers import CreateUserSerializer, Area_Pro, Area_City, CreaListSerializer


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


class AreaP(ListAPIView):
    queryset = Area.objects.filter(parent=None)
    serializer_class = Area_Pro


class AreaC(RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = Area_City


class Create_Area(ListCreateAPIView):
    serializer_class = CreaListSerializer

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

