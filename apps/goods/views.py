from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from goods.models import GoodsCategory, Goods
from goods.serializers import GoodsCategorySerializer, GoodsSlideSerializer, GoodsRecommendSerializer, GoodsSerializer, \
    GoodsBreadSerializer


class GoodsCategoryView(APIView):
    def get(self, request):
        queryset = GoodsCategory.objects.filter(parent_id__exact=0)
        serializer = GoodsCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class GoodsCategoryView2(APIView):
    def get(self, request):
        queryset = GoodsCategory.objects.filter(parent_id__exact=0)
        data_list = []
        for first_category in queryset:
            first_category_dict = GoodsCategorySerializer(first_category).data
            second_category_set = first_category.goodscategory_set.all()
            second_category_id_list = []
            for second_category in second_category_set:
                second_category_id_list.append(second_category.id)
            first_category_dict['red_goods'] = GoodsRecommendSerializer(
                Goods.objects.filter(category_id__in=second_category_id_list).order_by(
                    '-create_time')[0:5], many=True).data
            data_list.append(first_category_dict)
        return Response(data_list)


class GoodsSlideView(ListAPIView):
    queryset = Goods.objects.filter(is_slide__exact=1)
    serializer_class = GoodsSlideSerializer


class GoodsRecommendView(APIView):
    def get(self, request):
        queryset = Goods.objects.filter(is_red__exact=1)
        serializer = GoodsRecommendSerializer(queryset, many=True)
        return Response(serializer.data[0:4])


class GoodsListView(ReadOnlyModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指定过滤器
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 指定可以根据哪些字段进行列表数据的过滤
    filter_fields = ('category_id',)
    ordering_fields = ('sales', 'sell_price', 'create_time')


class GoodsBreadView(RetrieveAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsBreadSerializer
