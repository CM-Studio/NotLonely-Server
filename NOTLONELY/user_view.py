__author__ = 'yc'
# -*- coding:utf-8 -*-
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from user_auth import user_auth
from form import *
import json
import hashlib
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your views here.


@csrf_exempt
def register(request):
    responsedata={}
    stu_number_POST = request.POST['stu_number'].encode('utf-8')
    stu_password_POST = request.POST['stu_password'].encode('utf-8')
    username_POST = request.POST['username'].encode('utf-8')
    password_POST = request.POST['password'].encode('utf-8')
    repassword_POST = request.POST['repassword'].encode('utf-8')
    sex_POST = request.POST['sex'].encode('utf-8')
    nickname_POST = (request.POST['nickname']).encode('utf-8')
    qq_POST = request.POST['qq'].encode('utf-8')

    if not stu_number_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写信息门户账号'
    elif not stu_password_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写信息门户密码'
    elif not username_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写用户名'
    elif not password_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写密码'
    elif not sex_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请选择性别'
    elif not nickname_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写昵称'
    elif not qq_POST.strip():
        responsedata['status'] = '304'
        responsedata['msg'] = '请填写qq号码'
    elif User.objects.filter(stu_number = stu_number_POST):
        responsedata['status'] = '300'
        responsedata['msg'] = '该学号已被注册'.encode('utf-8')
    elif User.objects.filter(username = username_POST):
        responsedata['status'] = '301'
        responsedata['msg'] = str('该用户名已被注册').encode('utf-8')
    elif password_POST != repassword_POST:
        responsedata['status'] = '302'
        responsedata['msg'] = str('两次输入密码不一致').encode('utf-8')
#    elif user_auth(stu_number_POST, stu_password_POST) == -1:
#        responsedata['status'] = '303'
#        responsedata['msg'] = '信息门户学号或密码错误'
    else:
        password_POST = hashlib.md5(password_POST).hexdigest()
        user = User(stu_number = stu_number_POST, stu_password = stu_password_POST,
                    username = username_POST, password = password_POST, sex = sex_POST, nickname = nickname_POST,
                    qq = qq_POST)
        user.save()
        request.session['username'] = user.username
        responsedata['status'] = '0'
        responsedata['msg'] = '注册成功'
        responsedata['stu_number'] = user.stu_number
        responsedata['username'] = user.username
        responsedata['sex'] = user.sex
        responsedata['nickname'] = user.nickname
    return HttpResponse(json.dumps(responsedata, ensure_ascii=False, cls=DjangoJSONEncoder), content_type='application/json;charset=utf-8')

@csrf_exempt
def login(request):
    responsedata = {}
    if request.method == 'POST':
        username_POST = request.POST['username'].encode('utf-8')
        password_POST = request.POST['password'].encode('utf-8')
        userList = User.objects.filter(username = username_POST)
        if userList:
            user = userList[0]
            if hashlib.md5(password_POST).hexdigest() == user.password:
                request.session['username'] = username_POST
                responsedata['status'] = '0'
                responsedata['msg']  = '登陆成功'
                responsedata['id'] = user.id
		responsedata['nickname'] = user.nickname
                responsedata['username'] = user.username
		responsedata['avatar'] = user.avatar.url
	        responsedata['sex'] = user.sex
	 	responsedata['phone'] = user.qq
		responsedata['session_id'] = request.session.session_key
            else:
                responsedata['status'] = '300'
                responsedata['msg'] = '密码错误'
        else:
            responsedata['status'] = '301'
            responsedata['msg'] = '该用户名未注册'
    return HttpResponse(json.dumps(responsedata, ensure_ascii=False, cls=DjangoJSONEncoder), content_type='application/json;charset=utf-8')

@csrf_exempt
def upload_avatar(request):
    responseData = {}
    if request.method == 'POST':
        # form = ImageUploadForm( request.POST, request.FILES )
        # if form.is_valid():
        #     username_session = request.session['username']
        #     print username_session
        #     userList = User.objects.filter(username = username_session)
        #     user = userList[0]
        #     user.avatar = form.cleaned_data['upload_avatar']
        #     user.save()
        #     responseData['status'] = '0'
        #     responseData['msg'] = 'OK'
        image = request.FILES['upload_avatar']
        if image:
            username_session = request.session['username']
            userList = User.objects.filter(username = username_session)
            user = userList[0]
            user.avatar = image
            user.save()
            responseData['status'] = '0'
            responseData['msg'] = '上传成功'
	    responseData['headImg'] = user.avatar.url
        else:
            responseData['status'] = '300'
            responseData['msg'] = 'error'
    return HttpResponse(json.dumps(responseData, ensure_ascii=False, cls=DjangoJSONEncoder), content_type='application/json;charset=utf-8')

#@csrf_exempt
#def return_avatar(request):
#    if request.method == 'GET'
#        response = 

@csrf_exempt
def userSetting(request):
    responsedata = {}
    if request.method == 'POST':
        username_session = request.session.get('username')
        userList = User.objects.filter(username = username_session)
        qq = request.POST['qq'].encode('utf-8')
        p2=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch=p2.match(qq)
        if not phonematch:
            responsedata['status'] = '301'
            responsedata['msg'] = '请输入正确的手机号码'
        elif userList:
            user = userList[0]
            nickname_POST = request.POST['nickname'].encode('utf-8')
            sex = request.POST['sex'].encode('utf-8')
            desc = request.POST['desc'].encode('utf-8')
            qq = request.POST['qq'].encode('utf-8')
            user.nickname = nickname_POST
            user.sex = sex
            user.desc = desc
            user.qq = qq
            user.save()
            responsedata['status'] = '0'
            responsedata['msg'] = '修改成功'
            responsedata['username'] = user.username
            responsedata['nickname'] = user.nickname
            responsedata['sex'] = user.sex
            responsedata['desc'] = user.desc
            responsedata['qq'] = user.qq
        else:
            responsedata['status'] = '300'
            responsedata['msg'] = '请先登录'
    return HttpResponse(json.dumps(responsedata, ensure_ascii=False, cls=DjangoJSONEncoder), content_type='application/json;charset=utf-8')

# @csrf_exempt
# def userInfoShow(request):
#     responsedata = {}
#     userInfo = {}
#     username_session = request.session.get('username')
#     userList = User.objects.filter(username = username_session)
#     if userList:
#         user = userList[0]
#         responsedata['status'] = '0'
#         userInfo['avatar'] = user.avatar
#         userInfo['nickname'] = user.nickname
#         userInfo['sex'] = user.sex
#         userInfo['desc'] = user.desc
#         userInfo['rose'] = user.rose
#         tags = user.tag.all()
#         userInfo['tag'] = tags
#         responsedata['userinfo'] = userInfo
#     else:
#         responsedata['status'] = '300'
#         responsedata['msg'] = '请先登录'
#     return HttpResponse(json.dumps(responsedata), content_type="application/json; charset='utf-8'")
#
