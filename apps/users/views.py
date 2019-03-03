from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, \
    RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User, Area, Address
from users.serializers import CreateUserSerializer, Area_Pro, Area_City, CreaListSerializer, UP_Serializer


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
        return Address.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'user_id': request.user.id,

            'addresses': serializer.data  # 列表

        })


class Update_Defadd(UpdateAPIView):
    serializer_class = UP_Serializer

    def get_object(self):
        return self.request.user


class DelAddr(RetrieveDestroyAPIView):
    serializer_class = CreaListSerializer
    queryset = Address.objects.all()
    # def get_object(self):
    #     return Address.objects.get(id=self.kwargs['pk'])
