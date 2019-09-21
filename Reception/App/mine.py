from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from App.models import User
from App.serializer import UserSerializer
from tools.mytoken import Token


class UserAPIView(RetrieveAPIView):
    queryset = User
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        print(action)
        if hasattr(self, action):
            func = getattr(self, action)
        else:
            raise APIException('请求错误')
        return func(request, *args, **kwargs)

    def register(self, request, *args, **kwargs):
        data = {key: value for key, value in request.data.items()}
        if data['password'] == data['repassword']:
            data['password_hash'] = make_password(data.get('password', '123'))
            data['username'] = data['email']
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'code': 1,
                'msg': '注册成功'
            })
        return Response({
            'code': 0,
            'msg': '注册失败'
        })

    def login(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        user = User.check_login(email=email, password=password)
        print(user)
        if user:
            token = Token.generate_token(pk=str(user.uid))
            cache.set('email', token)
            return Response({
                'code': 1,
                'msg': '登录成功',
                'token': token
            })
        return Response({
            'code': 0,
            'msg': '用户名或密码错误'
        })

    def check_email(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            return Response({
                'code': 0,
                'msg': 'Existed.'
            })
        else:
            return Response({
                'code': 1,
                'msg': 'Fine.'
            })

    def check_password(self, request, *args, **kwargs):
        password = request.data.get('password')
        repassword = request.data.get('repassword')

        if password != repassword:
            return Response({
                'code': 0,
                'msg': 'Differ.'
            })
        else:
            return Response({
                'code': 1,
                'msg': 'Fine.'
            })

