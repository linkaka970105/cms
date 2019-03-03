from rest_framework.serializers import ModelSerializer

from news.models import News, NewsCategory


class TopNewsSer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class SonCateNewsSer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ("id", "title")


class CateNewsSer(ModelSerializer):
    newscategory_set = SonCateNewsSer(many=True, read_only=True)

    class Meta:
        model = NewsCategory
        fields = ("id", "title", "newscategory_set")
