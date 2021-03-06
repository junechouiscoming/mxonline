# -*- encoding:utf-8 -*-
"""课程信息"""

from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.TextField(verbose_name=u'课程描述')
    detail = UEditorField(width=600, height=300, imagePath="courses/ueditor", filePath="courses/ueditor",
                          default='', verbose_name=u'课程详情')
    degree = models.CharField(max_length=5, choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), verbose_name=u'难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name=u'封面图')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=20, verbose_name=u'课程标签')
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name=u'授课讲师')
    need_know = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    teacher_told_you = models.CharField(default='', max_length=300, verbose_name=u'老师告诉你')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否为轮播图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_chapter_nums(self):
        return self.lesson_set.all().count()

    # 获取课程所有章节
    def get_chapter(self):
        return self.lesson_set.all()


    # 获取课程学习人
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]


    def __str__(self):
        return '{0}'.format(self.name)


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    # 获取章节所有视频
    def get_video(self):
        return self.video_set.all()

    def __str__(self):
        return '{0}'.format(self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.URLField(default='', verbose_name=u'视频地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.name)
