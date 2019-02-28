from time import sleep

from asy_clelry.main import celery
from libs.yuntongxun.sms import CCP


@celery.task(name='send_sms')
def send_sms(mobile, sms_code):
    """获取短信验证码"""
    CCP().send_template_sms(mobile, [sms_code, 5], 1)
    print('获取短信验证码: %s' % (sms_code))
    sleep(5)

    return sms_code
