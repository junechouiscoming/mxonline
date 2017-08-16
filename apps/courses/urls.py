# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/08/15 15:04'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

]