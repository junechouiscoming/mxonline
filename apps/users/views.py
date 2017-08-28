import json

from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UpdateEmailForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import UploadImageForm
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # 判断表单
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 判断用户名和密码是否存在数据库中
            user = authenticate(username=user_name, password=pass_word)
            # 判断用户是否存在
            if user is not None:
                # 调用login方法
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 取出post请求中的username和password数据
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '用户已存在'})
            else:
                pass_word = request.POST.get('password', '')
                user_profile = UserProfile()
                # 给user_profile实例赋值
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                # 存入数据库中
                user_profile.save()

                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = '欢迎注册'
                user_message.save()

                send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'fogetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'fogetpwd_form': forgetpwd_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    '''登录界面修改密码'''
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwd_form': modifypwd_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
        })

    def post(self,request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps(user_info_form.errors),
                content_type='application/json'
            )


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(
                '{"status":"success", "msg":"修改成功"}',
                content_type='application/json'
            )
        else:
            return HttpResponse(
                '{"status":"fail"}',
                content_type='application/json'
            )


class UpdatePwdView(View):
    '''登录界面修改密码'''
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status":"fail", "msg":"密码不一致"}',
                    content_type='application/json'
                )
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse(
                '{"status":"success", "msg":"修改成功"}',
                content_type='application/json'
            )
        else:
            return HttpResponse(
                '{"status":"fail", "msg":"修改错误"}',
                content_type='application/json'
            )


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"email":"该邮箱已存在"}',
                content_type='application/json'
            )
        else:
            send_register_email(email, send_type='sendemail_code')
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json'
            )


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        update_email = UpdateEmailForm(request.POST, instance=request.user)

        if update_email.is_valid():
            email = request.POST.get('email')
            code = request.POST.get('code')
            if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='sendemail_code'):
                user = request.user
                user.email = email
                user.save()
                EmailVerifyRecord.objects.get(code=code).delete()
                return HttpResponse(
                    '{"status":"success"}',
                    content_type='application/json'
                )
            else:
                return HttpResponse(
                    '{"email":"验证码错误"}',
                    content_type='application/json'
                )
        else:
            return HttpResponse(
                '{"status":"fail", "email":"邮箱修改失败"}',
                content_type='application/json'
            )


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        my_courses = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {
            'my_courses': my_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        user = request.user
        myfav_orgs = UserFavorite.objects.filter(user=user, fav_type=2)
        for myfav_org in myfav_orgs:
            org_id = myfav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        user = request.user
        myfav_teachers = UserFavorite.objects.filter(user=user, fav_type=3)
        for myfav_teacher in myfav_teachers:
            teacher_id = myfav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        user = request.user
        myfav_courses = UserFavorite.objects.filter(user=user, fav_type=1)
        for myfav_course in myfav_courses:
            course_id = myfav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        msgs = UserMessage.objects.all().update(has_read=True)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages,
            'msgs': msgs,
        })


class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all()
        banner_courses = Course.objects.filter(is_banner=True)[:5]
        common_courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'banners': banners,
            'banner_courses': banner_courses,
            'common_courses': common_courses,
            'orgs': orgs,
        })


def page_404(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_500(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response