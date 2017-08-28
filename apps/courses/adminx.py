# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/08/08 16:07'

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image',
                    'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'image', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image',
                   'click_nums', 'fav_nums', 'add_time']
    readonly_fields = ['click_nums', 'fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['desc', 'degree']
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset().filter(is_banner=False)
        return qs


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image',
                    'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'image', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image',
                   'click_nums', 'fav_nums', 'add_time']
    readonly_fields = ['click_nums', 'fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset().filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)