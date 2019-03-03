import re

from django_redis import get_redis_connection
from redis.client import StrictRedis

from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Area, Address


class CreateUserSerializer(ModelSerializer):
    password2 = serializers.CharField(label='确认密码', min_length=8, max_length=20, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)
    allow = serializers.BooleanField(label='是否同意协议', default=False, write_only=True)

    token = serializers.CharField(label='登录状态token', read_only=True)

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        return value

    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请同意协议')
        return value

    def validate(self, attrs):
        password2 = attrs['password2']
        password = attrs['password']
        if password != password2:
            raise serializers.ValidationError('两次输入密码不一致')

        mobile = attrs['mobile']
        strict_redis = get_redis_connection('verify_codes')  # type: StrictRedis
        redis_smscode = strict_redis.get('sms_%s' % mobile)
        if redis_smscode is None:
            raise serializers.ValidationError('验证码无效')

        user_code = attrs['sms_code']
        if redis_smscode.decode() != user_code:
            raise serializers.ValidationError('验证码输入错误')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile')
        )
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法(函数)

        payload = jwt_payload_handler(user)  # 生成payload, 得到字典
        token = jwt_encode_handler(payload)  # 生成jwt字符串
        user.token = token
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow', 'token')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }


class Area_Pro(ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class Area_City(ModelSerializer):
    subs = Area_Pro(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


class CreaListSerializer(ModelSerializer):
    """序列时返回区域名称给前端"""
    province = StringRelatedField(label='省', read_only=True)

    city = StringRelatedField(label='市', read_only=True)
    district = StringRelatedField(label='区', read_only=True)
    """反序列时需要给字段增加外键"""
    province_id = serializers.IntegerField(label='省id', write_only=True)
    city_id = serializers.IntegerField(label='市id', write_only=True)
    district_id = serializers.IntegerField(label='区id', write_only=True)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_mobile(self, value):
        """验证手机号"""

        #         if not re.match(r'^1[3-9]\d{9}$', value):
        #             raise serializers.ValidationError('手机号格式错误')
        return value

    class Meta:
        model = Address
        exclude = ('create_time', 'update_time', 'is_deleted', 'user')


class UP_Serializer(serializers.Serializer):
    default_address_id = serializers.IntegerField(label='默认地址id', write_only=True)

    def validate_default_address_id(self, value):
        try:
            Address.objects.get(id=value, user=self.context['request'].user.id)
        except:
            raise serializers.ValidationError('地址id错误')
        return value

    def update(self, instance, validated_data):
        # id = validated_data['default_address_id']
        # a = Address.objects.get(id=id)
        # model写了外键，实际对象，表里存的这个对象id，
        # 修改或者新增数据，可以使用外键=对象，或者外键_id=对象id
        # instance.default_address = a
        instance.default_address_id = validated_data['default_address_id']

        instance.save()
        return validated_data
