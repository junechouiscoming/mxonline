# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/08/21 17:00'

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 用户主界面
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='user_image'),

    # 用户个人中心密码修改
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 用户个人中心邮箱发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 用户个人中心邮箱修改
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 用户个人中心我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 用户个人中心我的收藏-课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 用户个人中心我的收藏-授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 用户个人中心我的收藏-公开课
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 用户个人中心我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]