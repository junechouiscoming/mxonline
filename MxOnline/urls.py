"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, RegisterView, ActiveView, ForgetPwdView, ResetView, ModifyView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),

    # 用户相关
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url('^active/(?P<active_code>\w+)/$', ActiveView.as_view(), name='active'),
    url('^forget/$', ForgetPwdView.as_view(), name='forget'),
    url('^reset/(?P<reset_code>\w+)/$', ResetView.as_view(), name='reset'),
    url('^modify_pwd/$', ModifyView.as_view(), name='modify'),

    # 课程机构URL配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关URL配置
    url(r'^course/', include('courses.urls', namespace='course')),

    # 配置上传文件的访问处理函数
    url('^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),



]
