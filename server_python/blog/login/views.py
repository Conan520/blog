# coding=utf-8

from django.http import HttpResponse
from loguru import logger
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid

from .auth import CustomJSONWebTokenAuthentication
# from login.models import Admin


# Create your views here.


# FBV
# def login(request: HttpRequest) -> HttpResponse:
#     op(request.body)
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         account = data.get('account')
#         password = data.get('password')
#         print(f"account = {account}")
#         print(f"password = {password}")
#         return HttpResponse({'received data': data})
#     elif request.method == 'GET':
#         return HttpResponse("Get 请求")
#
#     else:
#         return HttpResponse(status=404)


# class AdminSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Admin
#         exclude = ['password']


# class LoginView(APIView):
#
#     def post(self, request: Request) -> HttpResponse:
#         logger.info(f"data = {request}")
#         admin = Admin.objects.filter(account=request.data["account"], password=request.data["password"]).first()
#         logger.info(f"admin = {admin}")
#         if admin is not None:
#             token = uuid.uuid4().hex
#             logger.info(f"token = {token}")
#             admin.token = token
#             admin.save()
#             admin_serializer = AdminSerializer(admin, many=False)
#             return Response({"code": 200, "msg": "登录成功", "data": admin_serializer.data}, status=200)
#             # return Response(admin_serializer.data, status=200)
#
#         return Response({"code": 401, "msg": "账号或密码错误", "data": ""}, status=200)

        # return HttpResponse(request.data)
from .serializers import LoginSerializer

class LoginView(APIView):

    def post(self, request: Request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            refresh = serializer.context.get('refresh')
            access = serializer.context.get('access')
            return Response({
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "refresh": refresh,
                    "access": access,
                    "username": serializer.data['username'],
                }})
        return Response({"code": 1004, "msg": "账号或密码错误", "refresh": "", "access": ""})
