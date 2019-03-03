from time import sleep

from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
import random

import logging

from asy_clelry.sms.tasks import send_sms

from libs.yuntongxun.sms import CCP
from users.models import Area
from users.serializers import Area_Pro

logger = logging.getLogger('django')


class SmsCodeView(APIView):
    # /sms_codes/1360xxx/
    def get(self, request, mobile):
        strict_redis = get_redis_connection('verify_codes')  # type: StrictRedis

        # 4. 校验短信验证码是否重复发送(1分钟内禁止重复发送)
        send_flag = strict_redis.get('send_flag_%s' % mobile)
        if send_flag:
            # return Response({'message': '频繁获取短信验证码'}, status=400)
            raise ValidationError({'message': '频繁获取短信验证码'})

        # 1. 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)  # 000123
        logger.info('短信验证码: %s   %s' % (mobile, sms_code))
        print(sms_code)

        # # 2. 发送短信验证码(云通讯)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # sleep(5)
        # 使用celery来发送短信, 可以解决阻塞问题



        # send_sms.delay('mobile', 'sms_code')

        # 3. 保存短信验证码
        # sms_13600000001        111111      （验证码：5分钟过期）
        # sms_13600000002        222222      （验证码：5分钟过期）
        # send_flag_13600000001        1      （发送标识：1 分钟过期）
        # send_flag_13600000002        1      （发送标识：1 分钟过期）

        # 方式1:
        # strict_redis.setex('sms_%s' % mobile, 60*5, sms_code)
        # strict_redis.setex('send_flag_%s' % mobile, 60, 1)

        # 方式2: 使用管道优化代码
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_%s' % mobile, 60 * 5, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        result = pipeline.execute()  # 列表
        print(result)

        # 5. 响应数据
        return Response({'message': 'OK'})


