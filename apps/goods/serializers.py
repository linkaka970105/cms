# 作者: python
# 日期: 19-2-27 上午11:55
# 工具: PyCharm
# Python版本：3.5.2
"""

"""
from rest_framework import serializers

from goods.models import GoodsCategory, Goods, GoodsAlbum


class GoodsAlbumSerialer(serializers.ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = ('id', 'thumb_path', 'original_path')


class GoodsRecommendSerializer(serializers.ModelSerializer):
    goodsalbum_set = GoodsAlbumSerialer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'create_time', 'goodsalbum_set')


class GoodsCategorySonSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title')


class GoodsListSerializer2(serializers.ModelSerializer):
    goods_set = GoodsRecommendSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'goods_set')


class GoodsCategorySerializer(serializers.ModelSerializer):
    goodscategory_set = GoodsCategorySonSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'goodscategory_set')


class GoodsSlideSerializer(serializers.ModelSerializer):
    goodsalbum_set = GoodsAlbumSerialer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'goodsalbum_set')


class GoodsSerializer(serializers.ModelSerializer):
    goodsalbum_set = GoodsAlbumSerialer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'goodsalbum_set', 'market_price', 'sell_price', 'stock', 'sub_title', 'goods_no')


class CateBreadFatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title')


class CateBreadSerializer(serializers.ModelSerializer):
    parent = CateBreadFatherSerializer(read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'title', 'parent')


class GoodsBreadSerializer(serializers.ModelSerializer):
    category = CateBreadSerializer(read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'category')
