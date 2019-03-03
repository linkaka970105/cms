from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from rest_framework.views import APIView

from news import serializers
from news.models import News, NewsCategory


class NewsTopView(APIView):
    def get(self, request):
        # 轮播图新闻
        slide_news = News.objects.filter(is_slide=True).exclude(img_url='')
        # 推荐新闻
        top_news = News.objects.order_by('-create_time')[0:10]
        # 图片新闻
        image_news = News.objects.exclude(img_url='').order_by('-click')[0:4]

        slide_news = serializers.TopNewsSer(slide_news, many=True).data
        top_news = serializers.TopNewsSer(top_news, many=True).data
        image_news = serializers.TopNewsSer(image_news, many=True).data
        data = {
            "slide_news": slide_news,
            "top_news": top_news,
            "image_news": image_news,
        }

        return Response(data)


class NewsCateView(APIView):
    def get(self, request):
        cate_query = NewsCategory.objects.filter(parent_id=0)
        # cate_query_list = serializers.CateNewsSer(cate_query, many=True).data
        data_dict = []
        for cate in cate_query:
            cate_query_dict = serializers.CateNewsSer(cate).data
            cate_next = cate.newscategory_set.all()

            ids_list = []
            for cate in cate_next:
                ids_list.append(cate.id)

                cate_query_dict['news'] = serializers.TopNewsSer(
                    News.objects.filter(category_id__in=ids_list).exclude(img_url='').order_by('-create_time')[0:4],
                    many=True).data

                cate_query_dict['top8'] = serializers.TopNewsSer(
                    News.objects.filter(category_id__in=ids_list).order_by('-click')[0:8], many=True).data
                data_dict.append(cate_query_dict)

        return Response(data_dict)
