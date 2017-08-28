# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/08/09 17:56'

from random import Random

from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    if send_type == 'sendemail_code':
        code = random_str(4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击下面的链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '密码重置链接'
        email_body = '请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'sendemail_code':
        email_title = '更换邮箱链接'
        email_body = '更换邮箱验证码：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass