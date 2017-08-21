# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/08/21 17:00'

from django.conf.urls import url
from .views import UserInfoView, UploadImageView

urlpatterns = [
    # 用户主界面
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='user_image')
]