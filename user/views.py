import hashlib
import random
import string
import traceback
import uuid
from urllib import response

from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect

from captcha.image import ImageCaptcha
from user.models import TUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import settings
# Create your views here.


def login(request):
    # 登录逻辑
    username = request.COOKIES.get("username")
    if username:
        username = username.encode("latin-1").decode("utf-8")
        password = request.COOKIES.get("password")
        user = TUser.objects.filter(name=username,password=password)
        if user:
            request.session["is_login"] = True
            return redirect("course:index")
        return render(request,'user/login.html')
    return render(request, 'user/login.html')


def active(request):
    try:
        # 账号激活
        token = request.GET.get("token")
        ser = Serializer(settings.SECRET_KEY,expires_in=180)
        id = ser.loads(token).get("id")
        user = TUser.objects.get(id=id)
        user.is_active = 1
        user.save()
        return render(request, 'user/login.html')
    except:
        return render(request, 'user/login.html')


def login_sql(request):
    try:
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        remember = request.POST.get("remember")
        user = TUser.objects.get(name=username)
        if user:
            # 加盐
            salt = user.salt
            # 将密码加密
            # 第一次加密,md5加密
            sha = hashlib.md5()
            sha.update((password + salt).encode())
            password = sha.hexdigest()
            # 第二次加密,sha加密
            sha = hashlib.sha256()
            sha.update((password + salt).encode())
            password = sha.hexdigest()
            if str(password) != str(user.password):
                return HttpResponse("yes_no")
            if user.is_active == 1:
                request.session["is_login"] = True
                resp = HttpResponse("yes")
                if remember:
                    username = username.encode("utf-8").decode("latin-1")
                    resp.set_cookie("username", username, max_age=3600 * 24 * 7)
                    resp.set_cookie("password", password, max_age=3600 * 24 * 7)
                else:
                    username = username.encode("utf-8").decode("latin-1")
                    resp.set_cookie("username", username)
                    resp.set_cookie("password", password)
                return resp
            # 对id进行加密
            ser = Serializer(settings.SECRET_KEY,expires_in=180)
            result = ser.dumps({"id":user.id})
            # 发送邮件
            send_mail("账号激活", "用户" + username + "请求激活账号,链接为：http://127.0.0.1:8000/user/active/?token=" + result.decode('utf-8'),
                      '1127104426@qq.com', ['1127104426@qq.com'])
            return HttpResponse("yes_yes_no")
        return HttpResponse("no")
    except:
        traceback.print_exc()
        return HttpResponse("no")


def register(request):
    return render(request,'user/register.html')


def register_sql(request):
    try:
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        # 判断是否存在
        user = TUser.objects.filter(name=username)
        if user:
            return HttpResponse("exist")
        # 不存在则创建新的用户
        with transaction.atomic():
            # 加盐
            salt = str(uuid.uuid4())
            # 将密码加密
            # 第一次加密,md5加密
            sha = hashlib.md5()
            sha.update((password + salt).encode())
            password = sha.hexdigest()
            # 第二次加密,sha加密
            sha = hashlib.sha256()
            sha.update((password + salt).encode())
            password = sha.hexdigest()
            TUser.objects.create(name=username,password=password,email=email,is_active=0,salt=salt)
            # 对id进行加密
            user = TUser.objects.filter(name=username)
            ser = Serializer(settings.SECRET_KEY,expires_in=180)
            result = ser.dumps({"id":user[0].id})
            # 发送邮件
            send_mail("账号激活", "用户" + username + "请求激活账号,链接为：http://127.0.0.1:8000/user/active/?token=" + result.decode('utf-8'),
                      '1127104426@qq.com', ['1127104426@qq.com'])
            return HttpResponse("yes")
    except:
        traceback.print_exc()
        return HttpResponse("no")


# 用户名逻辑
def register_username(request):
    try:
        username = request.POST.get("user_name")
        user = TUser.objects.filter(name=username)
        if user:
            return HttpResponse("no")
        return HttpResponse("yes")
    except:
        traceback.print_exc()
        return HttpResponse("no")


def register_captcha(request):
    try:
        code = request.POST.get("code")
        if code.lower() == request.session.get("code").lower():
            return HttpResponse("yes")
        return HttpResponse("no")
    except:
        traceback.print_exc()
        return HttpResponse("no")


# 验证码逻辑
def get_captcha(request):
    # 声明一个验证码对象
    image = ImageCaptcha()
    # 生成随机码
    code = random.sample(string.ascii_letters+string.digits,4)
    code = "".join(code)
    print("验证码", code)
    request.session['code'] = code
    # 将验证码写入图片
    data = image.generate(code)
    return HttpResponse(data, 'image/png')


# 找回密码
def forget_pwd(request):
    return render(request,'user/forget_pwd.html')


def forget_sql(request):
    try:
        username = request.POST.get("user_name")
        email = request.POST.get("email")
        user = TUser.objects.filter(name=username)
        if user:
            if user[0].email == email:
                request.session["username"] = username
                return HttpResponse("yes")
            return HttpResponse("yes_no")
        return HttpResponse("no")
    except:
        traceback.print_exc()
        return HttpResponse("no")


# 退出登录
def logout(request):
    # 清楚cookie
    resp = render(request,'user/logout.html')
    resp.delete_cookie("username")
    resp.delete_cookie("password")
    return resp


# 重置密码
def reset_pwd(request):
    return render(request,'user/reset_pwd.html')


def reset_pwd_sql(request):
    try:
        username = request.session.get("username")
        password = request.POST.get("pwd")
        user = TUser.objects.get(name=username)
        # 加盐
        salt = user.salt
        # 将密码加密
        # 第一次加密,md5加密
        sha = hashlib.md5()
        sha.update((password + salt).encode())
        password = sha.hexdigest()
        # 第二次加密,sha加密
        sha = hashlib.sha256()
        sha.update((password + salt).encode())
        password = sha.hexdigest()
        with transaction.atomic():
            user.password = password
            user.is_active = 0
            user.save()
            return HttpResponse("yes")
    except:
        return HttpResponse("no")
