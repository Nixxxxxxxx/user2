import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.models import User


def register(request):
    # get访问和post访问
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 客户post访问，接受客户端json数据，保存信息到数据库
        res_data = json.loads(request.body)
        username = res_data['username']
        password = res_data['password']

        user = User.objects.create(username=username, password=password)

        return redirect('/login/')


def login(request):
    # 保存用户状态信息，使用session，客户登录成功之后，设置session发送给客户端
    # 客户端下次访问如果带着session数据，则提示客户已经登录了
    username = request.session.get('username', '')
    if username:
        return HttpResponse("<h1>请勿重复登陆<h1/>")

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 客户post登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return JsonResponse({"message": "login in lose"})
        else:
            # 登陆成功，设置session，从数据库里面取出客户信息
            request.session['user_id'] = user.id
            request.session['username'] = username

            if remember != 'true':
                # 会话结束，销毁session
                request.session.set_expiry(0)

            return JsonResponse({"message": "login in success"})


def user_info(request, id):
    """接受资源路径带参数的访问"""
    # 根据客户端传入的id， 找到数据库对应的客户信息，以json的数据格式发给客户端
    user = User.objects.get(id=id)
    user_dict = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'gender': user.gender,
        'age': user.age
    }

    return JsonResponse(user_dict)


class LoginView(View):
    def get(self,request):
        # 保存用户状态信息，使用session，客户登录成功之后，设置session发送给客户端
        # 客户端下次访问如果带着session数据，则提示客户已经登录了
        username = request.session.get('username', '')
        if username:
            return HttpResponse("<h1>请勿重复登陆<h1/>")

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return JsonResponse({"message": "login in lose"})
        else:
            # 登陆成功，设置session，从数据库里面取出客户信息
            request.session['user_id'] = user.id
            request.session['username'] = username

            if remember != 'true':
                # 会话结束，销毁session
                request.session.set_expiry(0)

            return JsonResponse({"message": "login in success"})